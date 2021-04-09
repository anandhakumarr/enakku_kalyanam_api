from django.contrib.auth.models import User
import graphene
from graphene_django import DjangoObjectType
from graphene import ObjectType
from api.models import UserProfile, UserFamily, PartnerPreference
from api.schemas.validation import Validation
from api.schemas.descriptions import *
from api.schemas.utils import *
from graphql import GraphQLError
from django.db.models import Q
from django.contrib.auth import authenticate

class FamilyType(DjangoObjectType):
	class Meta:
		model = UserFamily
		exclude = ("id", "user",)


class PartnerPreferenceType(DjangoObjectType):
	class Meta:
		model = PartnerPreference
		exclude = ("id", "user",)


class UserProfileType(DjangoObjectType):
	class Meta:
		model = UserProfile
		exclude = ("id", "user", "is_editor", "otp", "email_otp", "mobile_otp")

	family = graphene.List(FamilyType)
	partner = graphene.List(PartnerPreferenceType)

	@staticmethod
	def resolve_family(root, info, **kwargs):
		family = UserFamily.objects.filter(user=info.context.user)
		return family

	@staticmethod
	def resolve_partner(root, info, **kwargs):
		partner = PartnerPreference.objects.filter(user=info.context.user)
		return partner

class UpdateProfile(graphene.Mutation):
    """ Mutation to UpdateProfile """

    message = graphene.String()
    status = graphene.String()

    class Arguments:
	    user_type = graphene.String(required=True)
	    name = graphene.String(required=True)
	    is_employed = graphene.Boolean(required=True)
	    occupation = graphene.String(required=True)


    def mutate(self, info, **kwargs):
        user = info.context.user
        Validation.check_user_login(user)

        profile = UserProfile.objects.get(user=user)
        profile.email_otp = token
        profile.save()

        return UpdateProfile(status='success', message='Profile details updated!')

class UpdatePartner(graphene.Mutation):
    """ Mutation to UpdatePartner """

    message = graphene.String()
    status = graphene.String()

    class Arguments:
	    user_type = graphene.String(required=True)
	    name = graphene.String(required=True)
	    is_employed = graphene.Boolean(required=True)
	    occupation = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        user = info.context.user
        Validation.check_user_login(user)

        profile = UserProfile.objects.get(user=user)
        profile.email_otp = token
        profile.save()

        return UpdatePartner(status='success', message='Partner details updated!')

class UpdateFamily(graphene.Mutation):
    """ Mutation to UpdateFamily """

    message = graphene.String()
    status = graphene.String()

    class Arguments:
	    user_type = graphene.String(required=True)
	    name = graphene.String(required=True)
	    is_employed = graphene.Boolean(required=True)
	    occupation = graphene.String(required=True)

    def mutate(self, info, user_type, name, is_employed, occupation, **kwargs):
        user = info.context.user
        user_type = user_type.title()
        Validation.check_user_login(user)
        Validation.validate_usertype(user_type)

        UserFamily.objects.create(user=user, user_type=user_type, name=name,
        	is_employed=is_employed, occupation=occupation)

        return UpdateFamily(status='success', message='Family details updated!')


class ProfileMutation(graphene.ObjectType):
    update_profile = UpdateProfile.Field()
    update_partner = UpdatePartner.Field()
    update_family  = UpdateFamily.Field()        


class ProfileQuery(graphene.ObjectType):
    """ Profile """
    profile = graphene.Field(UserProfileType,
    		  username=graphene.String())

    def resolve_profile(self, info, username=None):
        user = info.context.user
        Validation.check_user_login(user)
        if username:
        	user = User.objects.filter(username=username).first()
        	if not user:
        		raise GraphQLError("User not exist!")
        profile = UserProfile.objects.filter(user=user).first()
        return profile      
