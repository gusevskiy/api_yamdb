from django.shortcuts import get_object_or_404
from django.db.models import Avg
from .utils import (
    send_confirmation_email, validate_user_data_and_get_response,
    ConfirmationCodeManager
)
from reviews.models import Genre, User, Title, Category, Review
from .serializers import (
    GenreSerializer, CategorySerializer, UserSerializer,
    TitleReadSerializer, ReviewSerializer, CommentSerializer,
    UsersMeSerializer, TitleWriteSerializer
)
from .mixins import GetPostDeleteViewSet
from .permissions import (
    IsAdminOrReadOnly,
    UsersEndpointPermission,
    AuthorOrModeratorReadOnly,
    AuthorAndStaffOrReadOnly
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets

from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .filtersets import TitleFilterSet


confirmation_codes_manager = ConfirmationCodeManager()


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
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (UsersEndpointPermission,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        self.serializer_class = UsersMeSerializer
        self.permission_classes = (IsAuthenticatedOrReadOnly, )
        self.kwargs['username'] = request.user.username
        if request.method == 'GET':
            return self.retrieve(request)
        elif request.method == 'PATCH':
            return self.partial_update(request)

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
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterSet
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleWriteSerializer


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

    bad_response = validate_user_data_and_get_response(username, email)
    if bad_response is not None:
        return bad_response

    user = User.objects.get_or_create(
        username=username,
        email=email
    )[0]
    user.save()
    confirmation_code = confirmation_codes_manager.generate_code(username)
    confirmation_codes_manager.save_code(confirmation_code, username, email)

    send_confirmation_email(email, confirmation_code, username)

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

    if not confirmation_codes_manager.code_exists(username):
        return Response(
            {"error": "Please, request a code at /auth/signup/"},
            status.HTTP_404_NOT_FOUND
        )
    if confirmation_codes_manager.check_code(confirmation_code, username):
        token_pair = confirmation_codes_manager.get_tokens_for_user(username)
        return Response({"token": token_pair['access']}, status.HTTP_200_OK)

    return Response(
        {"error": "Wrong confirmation code! Please, request new code."},
        status.HTTP_400_BAD_REQUEST
    )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrModeratorReadOnly, )

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorAndStaffOrReadOnly, )

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        review_queryset = review.comments.all()
        return review_queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)
