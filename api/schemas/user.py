from django.contrib.auth.models import User
import graphene
from graphene_django import DjangoObjectType
from graphene import ObjectType
from api.models import UserProfile, UserDevice, Membership, Notification, MessageRoom
from api.schemas.validation import Validation
from api.schemas.descriptions import *
from api.schemas.utils import *
from graphql import GraphQLError
from django.db.models import Q
from django.contrib.auth import authenticate
import _thread

class ProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile

class RoomType(ObjectType):
    room_id = graphene.String()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")

    profile = graphene.List(ProfileType)

    @staticmethod
    def resolve_profile(root, info, **kwargs):
        profile = UserProfile.objects.filter(user=root)
        return profile

class NotificaitonObject(DjangoObjectType):
    class Meta:
        model = Notification
        exclude = ("user",)

class NotificationWrapper(ObjectType):
    results = graphene.List(NotificaitonObject)
    total_elements = graphene.Int()
    number_of_elements = graphene.Int()
    size = graphene.Int()
    total_pages = graphene.Int()
    current_page = graphene.Int()
    has_next_page = graphene.Boolean()

    class Meta:
        description = desc_wrapper


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
        device_id = kwargs.get('device_id', "")
        device_token = kwargs.get('device_token', "")
        device_type = kwargs.get('device_type', "")
        device_os = kwargs.get('device_os', "")
        device_version = kwargs.get('device_version', "")


        profile = UserProfile.objects.filter(primary_phone=phone).first()
        if profile:
            raise GraphQLError("Mobile already registered, Please Login!")

        device = UserDevice.objects.filter(device_id=device_id).first()
        if device:
            raise GraphQLError("Device already registered, Please Login!")

        try:
            user = User(first_name=first_name, last_name=last_name, email=email)
            user.set_password(password)
            user.save()
        except:
            raise GraphQLError("Email already registered, Please Login!")

        if device_id and device_type: 
            UserDevice.objects.create(user=user,device_id=device_id, device_token=device_token, 
                device_type=device_type, device_os=device_os, device_version=device_version)

        UserProfile.objects.create(user=user, primary_phone=phone)

        return Register(user=user)


class ResendEmailVerification(graphene.Mutation):
    """ Mutation to EmailVerification """

    message = graphene.String()
    status = graphene.String()

    def mutate(self, info, **kwargs):
        user = info.context.user
        Validation.check_user_login(user)

        token = random_token(6)

        profile = UserProfile.objects.get(user=user)
        profile.email_otp = token
        profile.save()

        _thread.start_new_thread( sendmail, ('verify_email',user.email, token, user.first_name) )

        return ResendEmailVerification(status='success', message='OTP successfully sent!')

class ResendMobileVerification(graphene.Mutation):
    """ Mutation to ResendMobileVerification """

    message = graphene.String()
    status = graphene.String()
    otp = graphene.String()

    def mutate(self, info, **kwargs):
        user = info.context.user
        Validation.check_user_login(user)

        token = random_token(6)

        profile = UserProfile.objects.get(user=user)
        profile.mobile_otp = token
        profile.save()

        return ResendMobileVerification(status='success', message='OTP successfully sent!', otp=token)

class ForgotPassword(graphene.Mutation):
    """ Mutation to ForgotPassword """

    message = graphene.String()
    status = graphene.String()

    class Arguments:
        email = graphene.String(required=True)

    def mutate(self, info, email, **kwargs):
        Validation.check_is_empty(email, 'Email')

        user = User.objects.filter(email=email).first()
        if not user:
            raise GraphQLError("Email not registered")

        token = random_token(6)

        profile = UserProfile.objects.get(user=user)
        profile.otp = token
        profile.save()

        _thread.start_new_thread( sendmail, ('forgot_password', email, token, user.first_name) )

        return ForgotPassword(status='success', message='OTP successfully sent!')


class VerifyOTP(graphene.Mutation):
    """ Mutation to VerifyOTP """

    message = graphene.String()
    status = graphene.String()

    class Arguments:
        otp = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, otp, email, **kwargs):
        Validation.check_is_empty(email, 'Email')
        Validation.check_is_empty(otp, 'OTP')
        user = User.objects.get(email=email)
        if not user:
            raise GraphQLError("Email not registered")

        profile = UserProfile.objects.get(user=user)
        if profile.otp != otp:
            raise GraphQLError("Incorrect OTP, Please try again!")
        profile.otp = None
        profile.save()

        return VerifyOTP(status='success', message='OTP successfully verified!')


class ResetPassword(graphene.Mutation):
    """ Mutation to ResetPassword """

    message = graphene.String()
    status = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        newpassword = graphene.String(required=True)

    def mutate(self, info, email, newpassword, **kwargs):
        Validation.check_is_empty(email, 'Email')
        Validation.check_is_empty(newpassword, 'New Password')
        user = User.objects.get(email=email)
        if not user:
            raise GraphQLError("Email not registered")

        profile = UserProfile.objects.get(user=user)
        if profile.otp != None:
            raise GraphQLError("Please verify OTP!")

        user.set_password(newpassword)
        user.save()

        return ResetPassword(status='success', message='Password successfully updated!')



class VerifyEmailOTP(graphene.Mutation):
    """ Mutation to VerifyEmailOTP """

    message = graphene.String()
    status = graphene.String()

    class Arguments:
        otp = graphene.String(required=True)

    def mutate(self, info, otp, **kwargs):
        Validation.check_is_empty(otp, 'OTP')
        user = info.context.user
        Validation.check_user_login(user)

        profile = UserProfile.objects.get(user=user)
        if profile.email_otp != otp:
            raise GraphQLError("Incorrect OTP, Please try again!")
        profile.email_otp = None
        profile.email_verified = True
        profile.save()

        return VerifyEmailOTP(status='success', message='Email successfully verified!')

class VerifyMobileOTP(graphene.Mutation):
    """ Mutation to VerifyMobileOTP """

    message = graphene.String()
    status = graphene.String()

    class Arguments:
        otp = graphene.String(required=True)

    def mutate(self, info, otp, **kwargs):
        Validation.check_is_empty(otp, 'OTP')
        user = info.context.user
        Validation.check_user_login(user)

        profile = UserProfile.objects.get(user=user)
        if profile.mobile_otp != otp:
            raise GraphQLError("Incorrect OTP, Please try again!")
        profile.mobile_otp = None
        profile.phone_verified = True
        profile.save()

        return VerifyMobileOTP(status='success', message='Mobile successfully verified!')


class ChangePassword(graphene.Mutation):
    """ Mutation to ChangePassword """

    message = graphene.String()
    status = graphene.String()

    class Arguments:
        oldpassword = graphene.String(required=True)
        newpassword = graphene.String(required=True)

    def mutate(self, info, oldpassword, newpassword, **kwargs):

        user = info.context.user
        Validation.check_user_login(user)

        Validation.check_is_empty(oldpassword, 'Old Password')
        Validation.check_is_empty(newpassword, 'New Password')

        user_auth = authenticate(username=user.email, password=oldpassword)
        if user_auth is None:
            raise GraphQLError("Incorrect Old Password")

        user.set_password(newpassword)
        user.save()

        return ChangePassword(message='Password Changed!', status='success')


class UserMutation(graphene.ObjectType):
    register = Register.Field()
    change_password = ChangePassword.Field()
    reset_password = ResetPassword.Field()
    verify_otp = VerifyOTP.Field()
    forgot_password = ForgotPassword.Field()
    resend_email_verification = ResendEmailVerification.Field()
    resend_mobile_verification = ResendMobileVerification.Field()
    verify_email_otp = VerifyEmailOTP.Field()
    verify_mobile_otp = VerifyMobileOTP.Field()

class UserQuery(graphene.ObjectType):
    """ Me """
    me = graphene.Field(UserType)

    def resolve_me(self, info):
        user = info.context.user
        Validation.check_user_login(user)
        return user        

    """ Create/Get Chat room """
    get_chat_room = graphene.Field(RoomType,
                            user1=graphene.String(required=True),
                            user2=graphene.String(required=True),
                        )

    def resolve_get_chat_room(self, info, user1, user2, **kwargs):
        user = info.context.user
        Validation.check_user_login(user)

        user_count = User.objects.filter(username__in=[user1, user2]).count()
        if user_count != 2 or user1 == user2:
            raise GraphQLError("User matching Failed, Please contact admin!")

        room_res = MessageRoom.objects.filter(Q(user1__username=user1,user2__username=user2) | Q(user1__username=user2,user2__username=user1)).first()

        if room_res:
            room_id = room_res.id
        else:
            room_name = user1 + '|' + user2
            user1 = User.objects.get(username=user1)
            user2 = User.objects.get(username=user2)
            room = MessageRoom(user1=user1, user2=user2, room_name=room_name)
            room.save()
            room_id = room.id

        return {'room_id': room_id}


    """ Notification List """

    notification = graphene.Field(
                NotificationWrapper,
                size=graphene.Int(description=desc_size),
                page=graphene.Int(description=desc_page))

    def resolve_notification(self, info, size=100, page=1, **kwargs):
        Validation.check_user_login(info.context.user)
        qs = Notification.objects.filter(user=info.context.user).order_by('-updated_ts')
        return get_wrapper_details(NotificationWrapper, qs, page, size) 

