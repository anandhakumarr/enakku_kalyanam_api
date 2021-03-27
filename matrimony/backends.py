from django.contrib.auth import get_user_model
from api.models import UserProfile, UserDevice


class EmailBackend:
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is not None:
            UserModel = get_user_model()
            try:
                user = UserModel.objects.get(email__iexact=username)
            except UserModel.DoesNotExist:
                """Not found, try another backend"""
            else:
                if user.check_password(password) and user.is_active:
                    return user
        return None

class PhoneBackend:
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is not None:
            UserModel = get_user_model()
            try:
                user = UserModel.objects.get(userprofile__primary_phone__iexact=username)
            except UserModel.DoesNotExist:
                """Not found, try another backend"""
            else:
                if user.check_password(password) and user.is_active:
                    return user
        return None

class DeviceBackend:
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is not None:
            UserModel = get_user_model()
            try:
                # https://docs.djangoproject.com/en/3.1/topics/db/examples/many_to_one/
                userdevice = UserDevice.objects.filter(device_id=username).first()
                if userdevice:
                    user = userdevice.user
                    if user.check_password(password) and user.is_active:
                        return user
            except UserModel.DoesNotExist:
                """Not found, try another backend"""
        return None

