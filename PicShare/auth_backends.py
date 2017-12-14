from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured
from django.apps import apps


class CustomUserModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        try:
            user = self.user_class.objects.get(username=username)

            if user.check_password(password):
                return user
            else:
                return None

        except self.user_class.DoesNotExist:
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    return user
                else:
                    return None
            except User.DoesNotExist:
                return None

    def get_user(self, user_id):
        try:
            return self.user_class.objects.get(pk=user_id)
        except self.user_class.DoesNotExist:
            try:
                return User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return None

    @property
    def user_class(self):
        if not hasattr(self, '_user_class'):
            self._user_class = apps.get_model(app_label='PicShare',
                                              model_name='PicShurUser')
            if not self._user_class:
                raise ImproperlyConfigured('Could not get custom user model')
        return self._user_class
