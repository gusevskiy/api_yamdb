from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from reviews.models import Review, Comment, Title
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.mail import EmailMessage
from time import time
from hashlib import md5
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import (
    Genre,
    Category,
    User,
    Review,
    Comment,
    Title
)
from .serializers import (
    GenreSerializer,
    CategorySerializer,
    ReviewSerializer,
    CommentSerializer,
    TitleSerialiser,
    UsersSerializer,
    NotAdminSerializer
    
)
from .mixins import GetPostDeleteViewSet
from .permissions import (
    IsAdminOrReadOnly,
    IsRoleAdmin,
    IsRoleModerator,
    IsAuthorOrReadOnly,
    AuthorAndStaffOrReadOnly,
    AdminOnly
    )


class GenreViewSet(GetPostDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class CategoryViewSet(GetPostDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsRoleAdmin | IsRoleModerator | IsAuthorOrReadOnly,
    )
    
    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorAndStaffOrReadOnly,)
        
    def get_queryset(self):
        title = get_object_or_404(Review, pk=self.kwargs.get('post_id'))
        return title.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerialiser
    permission_classes = (IsAdminOrReadOnly, )


confirmation_codes = {}


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
    email = request.data["email"]
    username = request.data["username"]
    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "User with this username already exists!"},
            status.HTTP_400_BAD_REQUEST
        )
    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "User with this email already exists!"},
            status.HTTP_400_BAD_REQUEST
        )

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
    username = request.data["username"]
    confirmation_code = request.data["confirmation_code"]
    if username not in confirmation_codes.keys():
        return Response(
            {"error": "Please, request a code at /auth/signup/"},
            status.HTTP_400_BAD_REQUEST
        )

    right_code = confirmation_codes[username]["code"]
    if right_code == confirmation_code:
        user = User.objects.get_or_create(
            username=username,
            email=confirmation_codes[username]["email"]
        )
        user.save()
        token_pair = get_tokens_for_user(user)
        return Response({"token": token_pair['access']}, status.HTTP_200_OK)

    return Response(
        {"error": "Wrong confirmation code! Please, request new code."},
        status.HTTP_400_BAD_REQUEST
    )


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, AdminOnly,)
    lookup_field = 'username'
    # filter_backends = (SearchFilter, )
    search_fields = ('username', )

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UsersSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)
