# django
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

# models
from users.models import User


class CustomBackend(ModelBackend):
    """
    Authenticates against users.models.User
    """
    supports_inactive_user = True

    def authenticate(self, email, password, token=None):
        """ login using  the username validating with the password  or the
        token. If the token is used, then it's deleted

        """
        UserModel = get_user_model()

        if email:
            # stirp and lower the email, since it should be case insensitive
            # and emails don't have spaces
            email = email.strip().lower()

        try:
            user = UserModel._default_manager.get_by_natural_key(email)
        except UserModel.DoesNotExist:
            return None
        if password is not None:
            if user.check_password(password):
                return user
        if token:
            if user.token == token and len(token) == 30:
                user.token = ""
                user.is_active = True
                user.save()
                return user
        return None

    def get_user(self, user_id):
        """ returns the user using the id """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
