from django.contrib.auth import get_user_model

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
                user = UserModel.objects.get(userprofile__device__device_id__iexact=username)
            except UserModel.DoesNotExist:
                """Not found, try another backend"""
            else:
                if user.check_password(password) and user.is_active:
                    return user
        return None

