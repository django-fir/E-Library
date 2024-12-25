from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth.models import User
from django.db.models import Q


User_model = get_user_model()


class MyBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User_model.objects.get(Q(username=username) | Q(Q(
                email=username) & Q(email_verified=True)))
        except User_model.DoesNotExist:
            User_model().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
            else:
                return None

        # Check the username/password and return a user.
