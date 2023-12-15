import sys
from accounts.models import User, Token
import pdb
from django.contrib.auth.backends import ModelBackend

class PasswordlessAuthenticationBackend(ModelBackend):

    def authenticate(self, uid):
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            return None



    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
