from django.contrib.auth.backends import BaseBackend
from django.db.models import Q

from mod_user.models import LinguaUser


class LinguaBaseBackend(BaseBackend):
    def authenticate(self, request, username=None, email=None, password=None):
        try:
            user = LinguaUser.objects.get(username=username)
        except LinguaUser.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return LinguaUser.objects.get(pk=user_id)
        except LinguaUser.DoesNotExist:
            return None
