from django.core.mail import EmailMessage
import json

from reviews.models import User

from .serializers import UserSerializer
from time import time
from hashlib import md5
from rest_framework_simplejwt.tokens import RefreshToken


# Раз уж захотели без глобальных переменных, вот вам ООПшный вариант
class ConfirmationCodeManager():
    codes: list
    code_length: int

    def __init__(self, code_length=8):
        self.codes = {}
        self.code_length = code_length

    def code_exists(self, username: str) -> bool:
        return username in self.codes

    def check_code(self, code: str, username: str) -> bool:
        popped_code = self.codes.pop(username)
        return popped_code == code

    def generate_code(self, username: str) -> str:
        timestamp = time()
        code = md5((str(timestamp) + username).encode()).hexdigest()
        return code[:self.code_length]

    def save_code(self, code: str, username: str, email: str) -> None:
        self.codes[username] = {
            'code': code,
            'email': email
        }

    def get_tokens_for_user(self, username: str) -> dict:
        user = User.objects.get(username)
        del self.codes[username]
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


def send_confirmation_email(to, code, username):
    email_text = f'Hello, {username}! You requested confirmation code for \
        Yamdb. Confirmation code: {code}'
    email_message = EmailMessage(
        'Yamdb confirmation code', 'noreply@yamdb.ru', email_text, to=[to, ]
    )
    email_message.send()


def validate_user_data_and_get_response(username, email):
    serializer = UserSerializer(data={
        'username': username,
        'email': email
    })

    serializer.validate_username(username)
    serializer.validate({
        'username': username,
        'email': email
    })
    serializer.is_valid(True)


def exception_message_to_response(msg):
    return json.loads(msg)
