from django.core.mail import EmailMessage
import json

from reviews.models import User

from .serializers import UserSerializer
from rest_framework.serializers import ValidationError
from rest_framework import status
from rest_framework.response import Response
from time import time
from hashlib import md5
from rest_framework_simplejwt.tokens import RefreshToken


confirmation_codes = {}


def send_confirmation_email(to, code, username):
    email_text = f'Hello, {username}! You requested confirmation code for \
        Yamdb. Confirmation code: {code}'
    email_message = EmailMessage(
        'Yamdb confirmation code', 'noreply@yamdb.ru', email_text, to=[to, ]
    )
    email_message.send()


def code_exists(username):
    return username in confirmation_codes


def check_code(code, username):
    popped_code = confirmation_codes.pop(username)
    return popped_code == code


def save_code(code, username, email):
    confirmation_codes[username] = {
        'code': code,
        'email': email
    }


def generate_code(username):
    timestamp = time()
    code = md5((str(timestamp) + username).encode()).hexdigest()[:8]
    return code


def get_tokens_for_user(username):
    user = User.objects.get(username)
    del confirmation_codes[username]
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def validate_user_data_and_get_response(username, email):
    bad_fields = []
    errors = []

    serializer = UserSerializer(data={
        'username': username,
        'email': email
    })

    try:
        serializer.validate_username(username)
    except ValidationError as e:
        bad_fields.append('username')
        errors.append(e.detail['error'])
        pass

    try:
        serializer.validate_email(email)
    except ValidationError as e:
        bad_fields.append('email')
        errors.append(e.detail['error'])
        pass

    if len(bad_fields) > 0:
        resp = {}
        for f in bad_fields:
            resp[f] = []
        resp["errors"] = errors
        return Response(
            resp,
            status.HTTP_400_BAD_REQUEST
        )
    return None


def exception_message_to_response(msg):
    return json.loads(msg)
