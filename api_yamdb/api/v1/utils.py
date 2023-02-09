from django.core.mail import EmailMessage
import json

from .serializers import UserSerializer
from rest_framework.serializers import ValidationError
from rest_framework import status
from rest_framework.response import Response


def send_confirmation_email(to, code, username):
    email_text = f'Hello, {username}! You requested confirmation code for \
        Yamdb. Confirmation code: {code}'
    email_message = EmailMessage(
        'Yamdb confirmation code', 'noreply@yamdb.ru', email_text, to=[to, ]
    )
    email_message.send()


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
