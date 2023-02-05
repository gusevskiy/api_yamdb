from django.shortcuts import get_object_or_404
from django.db.models import Avg
from reviews.models import Genre, User, Title, Category, Comment
from .serializers import (
    GenreSerializer, CategorySerializer, UserSerializer, TitleSerializer,
    TitleSerializerGET, ReviewSerializer, CommentSerializer, UsersMeSerializer
)
from .mixins import GetPostDeleteViewSet
from .permissions import (
    IsAdminOrReadOnly,
    IsAdminOrNoPermission,
    AuthorOrModeratorReadOnly,
    AuthorAndStaffOrReadOnly,
    UsersMePermission
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.core.mail import EmailMessage
from time import time
from hashlib import md5

from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import validate_email, validate_slug
from django.core.exceptions import ValidationError
from rest_framework.exceptions import MethodNotAllowed
from django_filters.rest_framework import DjangoFilterBackend
from .filtersets import TitleFilterSet


class GenreViewSet(GetPostDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = (IsAdminOrNoPermission,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    def get_permissions(self):
        if self.kwargs.get('username') == 'me':
            return (UsersMePermission(),)
        return (IsAdminOrNoPermission(),)

    def get_object(self):
        if self.kwargs.get('username') == 'me':
            self.kwargs['username'] = self.request.user.username
        return super(UsersViewSet, self).get_object()

    def get_serializer_class(self):
        if self.kwargs.get('username') == 'me':
            return UsersMeSerializer
        return UserSerializer

    def update(self, request, *args, **kwargs):
        if (
            request.method == 'PUT'
        ):
            raise MethodNotAllowed(method='PUT')
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if self.get_serializer_class() == UsersMeSerializer:
            raise MethodNotAllowed(method='DELETE')
        return super().destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save(role=self.request.user.role)


class CategoryViewSet(GetPostDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterSet
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleSerializerGET
        return TitleSerializer


confirmation_codes = {}


def validate(validator, text):
    try:
        validator(text)
        return True
    except ValidationError:
        return False


def generate_code(username):
    timestamp = time()
    code = md5((str(timestamp) + username).encode()).hexdigest()[:8]
    return code


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
def signup(request):
    keys = request.data.keys()
    if "email" not in keys or "username" not in keys:
        resp = {
            "error": "These value wasnt provided. Read docs again ;)",
        }
        if "email" not in keys:
            resp["email"] = []
        if "username" not in keys:
            resp["username"] = []
        return Response(
            resp,
            status.HTTP_400_BAD_REQUEST
        )
    email = request.data["email"]
    username = request.data["username"]
    # Validate data
    validate_data = [
        {
            "name": "email",
            "valid": validate(validate_email, email) and not len(email) >= 254
        },
        {
            "name": "username",
            "valid": (
                validate(validate_slug, username)
                and not username == "me"
                and not len(username) >= 150
            )
        }
    ]
    resp = {}
    for d in validate_data:
        if not d["valid"]:
            resp[d["name"]] = []
    if len(resp.keys()) > 0:
        resp["error"] = "Invalid data!"
        return Response(
            resp,
            status.HTTP_400_BAD_REQUEST
        )
    if (
        User.objects.filter(email=email).exists()
        and not User.objects.filter(username=username).exists()
    ):
        return Response(
            {"error": "This email is already used by other user."},
            status.HTTP_400_BAD_REQUEST
        )
    if (
        not User.objects.filter(email=email).exists()
        and User.objects.filter(username=username).exists()
    ):
        return Response(
            {"error": "This username is already used by other user."},
            status.HTTP_400_BAD_REQUEST
        )
    user = User.objects.get_or_create(
        username=username,
        email=email
    )[0]
    user.save()
    confirmation_code = generate_code(username)
    confirmation_codes[username] = {
        'code': confirmation_code,
        'email': email
    }

    email_text = f'''
        Hello, {username}! You requested confirmation code for Yamdb.
        Confirmation code: {confirmation_code}
    '''
    email_message = EmailMessage(
        "Yamdb confirmation code", email_text, to=[email, ]
    )
    email_message.send()

    return Response({"email": email, "username": username}, status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    keys = request.data.keys()
    if "confirmation_code" not in keys or "username" not in keys:
        return Response(
            {
                "error": "These value wasnt provided. Read docs again ;)",
            },
            status.HTTP_400_BAD_REQUEST
        )
    username = request.data["username"]
    confirmation_code = request.data["confirmation_code"]
    if username not in confirmation_codes.keys():
        return Response(
            {"error": "Please, request a code at /auth/signup/"},
            status.HTTP_404_NOT_FOUND
        )

    right_code = confirmation_codes[username]["code"]
    if right_code == confirmation_code:
        user = User.objects.get(
            username=username
        )
        token_pair = get_tokens_for_user(user)
        return Response({"token": token_pair['access']}, status.HTTP_200_OK)

    return Response(
        {"error": "Wrong confirmation code! Please, request new code."},
        status.HTTP_400_BAD_REQUEST
    )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # pagination_class = CommentPaginator
    permission_classes = (AuthorOrModeratorReadOnly, )

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # pagination_class = CommentPaginator
    permission_classes = (AuthorAndStaffOrReadOnly, )

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        try:
            review = title.reviews.get(id=self.kwargs.get('review_id'))
        except TypeError:
            TypeError('Нет такого отзыва')
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        try:
            review = title.reviews.get(id=self.kwargs.get('review_id'))
        except TypeError:
            TypeError('Нет такого отзыва')
        serializer.save(author=self.request.user, review=review)
