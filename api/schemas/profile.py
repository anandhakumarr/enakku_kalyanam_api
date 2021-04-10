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
		gender = graphene.String()
		about_me = graphene.String()
		about_family = graphene.String()
		dob = graphene.DateTime()
		profile_created_by = graphene.String()
		country = graphene.String()
		city = graphene.String()
		state = graphene.String()
		work_location = graphene.String()
		native_location = graphene.String()
		gothram = graphene.String()
		college = graphene.String()
		height = graphene.Decimal()
		weight = graphene.Decimal()
		physical_status = graphene.String()
		body_type = graphene.String()
		eating_habits = graphene.String()	    
		drinking_habits = graphene.String()
		smoking_habits = graphene.String()
		mother_tongue = graphene.String()
		religion = graphene.String()
		caste = graphene.String()
		raasi = graphene.String()
		sub_caste = graphene.String()
		star = graphene.String()
		highest_education = graphene.String()
		employed_in = graphene.String()
		occupation =  graphene.String()
		dosham = graphene.String()

	def mutate(self, info, **kwargs):
		user = info.context.user
		Validation.check_user_login(user)

		try:
			instance = UserProfile.objects.filter(user=user).first()
			if not instance:
				instance = UserProfile.objects.create(user=user)

			mother_tongue = kwargs.get('mother_tongue', instance.mother_tongue)
			if mother_tongue:
				mother_tongue = Validation.validate_mother_tongue(mother_tongue)

			religion = kwargs.get('religion', instance.religion)
			if religion:
				religion = Validation.validate_religion(religion)

			caste = kwargs.get('caste', instance.caste)
			if caste:
				caste = Validation.validate_caste(caste)

			raasi = kwargs.get('raasi', instance.raasi)
			if raasi:
				raasi = Validation.validate_raasi(raasi)

			sub_caste = kwargs.get('sub_caste', instance.sub_caste)
			if sub_caste:
				sub_caste = Validation.validate_sub_caste(sub_caste)

			star = kwargs.get('star', instance.star)
			if star:
				star = Validation.validate_star(star)

			highest_education = kwargs.get('highest_education', instance.highest_education)
			if highest_education:
				highest_education = Validation.validate_highest_education(highest_education)

			occupation = kwargs.get('occupation', instance.occupation)
			if occupation:
				occupation = Validation.validate_occupation(occupation)

			instance.gender = kwargs.get('gender', instance.gender)
			instance.dob = kwargs.get('dob', instance.dob)
			instance.about_me = kwargs.get('about_me', instance.about_me)
			instance.about_family = kwargs.get('about_family', instance.about_family)
			instance.profile_created_by = kwargs.get('profile_created_by', instance.profile_created_by)
			instance.country = kwargs.get('country', instance.country)
			instance.city = kwargs.get('city', instance.city)
			instance.state = kwargs.get('state', instance.state)
			instance.work_location = kwargs.get('work_location', instance.work_location)
			instance.native_location = kwargs.get('native_location', instance.native_location)
			instance.gothram = kwargs.get('gothram', instance.gothram)
			instance.college = kwargs.get('college', instance.college)
			instance.height = kwargs.get('height', instance.height)
			instance.weight = kwargs.get('weight', instance.weight)
			instance.physical_status = kwargs.get('physical_status', instance.physical_status)
			instance.body_type = kwargs.get('body_type', instance.body_type)
			instance.eating_habits = kwargs.get('eating_habits', instance.eating_habits)
			instance.drinking_habits = kwargs.get('drinking_habits', instance.drinking_habits)
			instance.smoking_habits = kwargs.get('smoking_habits', instance.smoking_habits)
			instance.mother_tongue = mother_tongue
			instance.religion = religion
			instance.caste = caste
			instance.raasi = raasi
			instance.sub_caste = sub_caste
			instance.star = star
			instance.highest_education = highest_education
			instance.employed_in = kwargs.get('employed_in', instance.employed_in)
			instance.occupation = occupation
			instance.dosham = kwargs.get('dosham', instance.dosham)
			instance.save()

			status='success'
			message = 'Profile details updated!'
		except Exception as e:
			status = 'error'
			message = e

		return UpdateProfile(status=status, message=message)

class UpdatePartner(graphene.Mutation):
	""" Mutation to UpdatePartner """

	message = graphene.String()
	status = graphene.String()

	class Arguments:
		age_from = graphene.Int()
		age_to = graphene.Int()
		height_from = graphene.Decimal()
		height_to = graphene.Decimal()
		physical_status = graphene.String()
		body_type = graphene.String()
		eating_habits = graphene.String()	    
		drinking_habits = graphene.String()
		smoking_habits = graphene.String()
		mother_tongue = graphene.String()
		religion = graphene.String()
		caste = graphene.String()
		raasi = graphene.String()
		sub_caste = graphene.String()
		star = graphene.String()
		highest_education = graphene.String()
		employed_in = graphene.String()
		occupation =  graphene.String()
		income_from = graphene.Int()
		income_to = graphene.Int()
		dosham = graphene.String()
		about_partner = graphene.String()

	def mutate(self, info, **kwargs):
		user = info.context.user
		Validation.check_user_login(user)

		try:
			instance = PartnerPreference.objects.filter(user=user).first()
			if not instance:
				instance = PartnerPreference.objects.create(user=user)

			mother_tongue = kwargs.get('mother_tongue', instance.mother_tongue)
			if mother_tongue:
				mother_tongue = Validation.validate_mother_tongue(mother_tongue)

			religion = kwargs.get('religion', instance.religion)
			if religion:
				religion = Validation.validate_religion(religion)

			caste = kwargs.get('caste', instance.caste)
			if caste:
				caste = Validation.validate_caste(caste)

			raasi = kwargs.get('raasi', instance.raasi)
			if raasi:
				raasi = Validation.validate_raasi(raasi)

			sub_caste = kwargs.get('sub_caste', instance.sub_caste)
			if sub_caste:
				sub_caste = Validation.validate_sub_caste(sub_caste)

			star = kwargs.get('star', instance.star)
			if star:
				star = Validation.validate_star(star)

			highest_education = kwargs.get('highest_education', instance.highest_education)
			if highest_education:
				highest_education = Validation.validate_highest_education(highest_education)

			occupation = kwargs.get('occupation', instance.occupation)
			if occupation:
				occupation = Validation.validate_occupation(occupation)
	
			instance.age_from = kwargs.get('age_from', instance.age_from)
			instance.age_to = kwargs.get('age_to', instance.age_to)
			instance.height_from = kwargs.get('height_from', instance.height_from)
			instance.height_to = kwargs.get('height_to', instance.height_to)
			instance.physical_status = kwargs.get('physical_status', instance.physical_status)
			instance.body_type = kwargs.get('body_type', instance.body_type)
			instance.eating_habits = kwargs.get('eating_habits', instance.eating_habits)
			instance.drinking_habits = kwargs.get('drinking_habits', instance.drinking_habits)
			instance.smoking_habits = kwargs.get('smoking_habits', instance.smoking_habits)
			instance.mother_tongue = mother_tongue
			instance.religion = religion
			instance.caste = caste
			instance.raasi = raasi
			instance.sub_caste = sub_caste
			instance.star = star
			instance.highest_education = highest_education
			instance.employed_in = kwargs.get('employed_in', instance.employed_in)
			instance.occupation = occupation
			instance.income_from = kwargs.get('income_from', instance.income_from)
			instance.income_to = kwargs.get('income_to', instance.income_to)
			instance.dosham = kwargs.get('dosham', instance.dosham)
			instance.about_partner = kwargs.get('about_partner', instance.about_partner)
			instance.save()

			status='success'
			message = 'Partner details updated!'
		except Exception as e:
			status = 'error'
			message = e

		return UpdatePartner(status=status, message=message)


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

        try:
        	family = UserFamily.objects.filter(user=user, user_type=user_type).first()
        	if family:
        		family.name = name
        		family.is_employed = is_employed
        		family.occupation = occupation
        		family.save()
        	else:
	        	UserFamily.objects.create(user=user, user_type=user_type, name=name,
	        	is_employed=is_employed, occupation=occupation)
        	status = 'success'
        	message = 'Family details updated!'
        except Exception as e:
        	status = 'error'
        	message = e

        return UpdateFamily(status=status, message=message)

    # completed_basic_details = models.BooleanField(default=False)
    # completed_relegious_details = models.BooleanField(default=False)    
    # completed_professional_details = models.BooleanField(default=False)
    # completed_family_details = models.BooleanField(default=False)
    # completed_profile_details = models.BooleanField(default=False)

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
