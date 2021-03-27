from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType
from api.models import UserProfile, UserDevice, Membership
from api.schemas.validation import Validation

class ProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email")

    profile = graphene.List(ProfileType)

    @staticmethod
    def resolve_profile(root, info, **kwargs):
        profile = UserProfile.objects.filter(user=root)
        return profile


class Register(graphene.Mutation):
    """ Mutation to register a user """

    user = graphene.Field(UserType)    

    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=True)
        password = graphene.String(required=True)
        device_id = graphene.String()
        device_token = graphene.String()
        device_type = graphene.String()
        device_os = graphene.String()
        device_version = graphene.String()

    def mutate(self, info, name, email, phone, password, **kwargs):

        Validation.check_is_empty(name, 'Name')
        Validation.check_is_empty(password, 'Password')

        name_slice = name.split(" ")
        first_name = name_slice[0].title()
        last_name = ' '.join(name_slice[1:]) if len(name_slice) > 1 else ''
        name = name+'|'+phone

        user = get_user_model()(
            first_name=first_name,
            last_name=last_name,
            username=name,
            email=email,
        )
        user.set_password(password)
        user.save()

        membership = Membership.objects.get(membership='Free')


        device_id = kwargs.get('device_id', "")
        device_token = kwargs.get('device_token', "")
        device_type = kwargs.get('device_type', "")
        device_os = kwargs.get('device_os', "")
        device_version = kwargs.get('device_version', "")

        if device_id and device_type: 
            UserDevice.objects.create(user=user,device_id=device_id, device_token=device_token, 
                device_type=device_type, device_os=device_os, device_version=device_version)

        UserProfile.objects.create(user=user, primary_phone=phone, membership=membership)

        return Register(user=user)


# Verfify Email
# Verfify Mobile 
# ResetPassword
# ForgotPassword 
# ChangePassword

class UserMutation(graphene.ObjectType):
    register = Register.Field()

class UserQuery(graphene.ObjectType):
    me = graphene.Field(UserType)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user        