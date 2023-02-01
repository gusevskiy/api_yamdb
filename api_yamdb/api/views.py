"""from rest_framework import viewsets, serializers, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet"""

from reviews.models import Genre, User
from .serializers import GenreSerializer, UserSerializer
from .mixins import GetPostDeleteViewSet
from .permissions import IsAdminOrReadOnly, IsAdminOrNoPermission

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage
from time import time
from hashlib import md5
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets


class GenreViewSet(GetPostDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrNoPermission,)


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
    if username == "me":
        return Response(
            {"error": "You cant register a user with name 'me'"},
            status.HTTP_400_BAD_REQUEST
        )
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
