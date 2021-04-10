from graphql import GraphQLError
from api.models import *


class Validation:

	def check_user_login(user):
		if user.is_anonymous:
			raise GraphQLError("Account Not logged in!'")

	def check_staff_role(user):
		if not user.is_staff:
			raise GraphQLError("Operation Not Allowed, Please contact admin.")

	def check_editor_role(user):
		profile = UserProfile.objects.filter(user=user).first()
		if not profile or not profile.is_editor:
			raise GraphQLError("Operation Not Allowed, Please contact admin.")

	def check_is_list_empty(value, field):
		if value is None or value==[] or len(value) == 0 or value == ['']:
			raise GraphQLError("{0} field can't be empty".format(field.title()))

	def check_is_date_empty(value, field):
		if value is None or value=='':
			raise GraphQLError("{0} field can't be empty".format(field.title()))

	def check_is_empty(value, field):
		if value is None or value=='' or value.isspace():
			raise GraphQLError("{0} field can't be empty".format(field.title()))

	def validate_usertype(usertype):
		if usertype not in ['Mother', 'Father', 'Sister', 'Brother']:
			raise GraphQLError("Invalid user type, Please contact support.")

	def validate_dosham(dosham):
		if dosham not in ['Yes', 'No', "Doesn't Mater"]:
			raise GraphQLError("Invalid dosham, Please contact support.")

	def validate_drinking(drinking):
		if drinking not in ['Yes', 'No', "Occasionally"]:
			raise GraphQLError("Invalid drinking habbit, Please contact support.")

	def validate_eating(eating):
		if eating not in ['Vegetarian', 'Non-Vegetarian', "Eggetarian"]:
			raise GraphQLError("Invalid eating habbit, Please contact support.")

	def validate_bodytype(bodytype):
		if bodytype not in ['Average', 'Athletic', "Slim", "Heavy"]:
			raise GraphQLError("Invalid bodytype, Please contact support.")

	def validate_employment(employment):
		if employment not in ['Private', 'Business', "Defence", "Self Employed", "Not Working", "Government/PSU"]:
			raise GraphQLError("Invalid employment, Please contact support.")

	def validate_mother_tongue(mother_tongue):
		mothertongue = MotherTongue.objects.filter(title=mother_tongue).first()
		if not mothertongue:
			raise GraphQLError("Invalid mother_tongue, Please contact support.")
		else:
			return mothertongue

	def validate_religion(religion):
		religion = Religion.objects.filter(title=religion).first()
		if not religion:
			raise GraphQLError("Invalid religion, Please contact support.")
		else:
			return religion

	def validate_caste(caste):
		caste = Caste.objects.filter(title=caste).first()
		if not caste:
			raise GraphQLError("Invalid caste, Please contact support.")
		else:
			return caste

	def validate_raasi(caste):
		raasi = Raasi.objects.filter(title=raasi).first()
		if not raasi:
			raise GraphQLError("Invalid raasi, Please contact support.")
		else:
			return raasi

	def validate_sub_caste(sub_caste):
		sub_caste = SubCaste.objects.filter(title=sub_caste).first()
		if not sub_caste:
			raise GraphQLError("Invalid sub_caste, Please contact support.")
		else:
			return sub_caste

	def validate_star(star):
		star = Star.objects.filter(title=star).first()
		if not star:
			raise GraphQLError("Invalid star, Please contact support.")
		else:
			return star

	def validate_highest_education(highest_education):
		highest_education = Star.objects.filter(title=highest_education).first()
		if not highest_education:
			raise GraphQLError("Invalid highest_education, Please contact support.")
		else:
			return highest_education

	def validate_occupation(occupation):
		occupation = OccupationCategory.objects.filter(title=occupation).first()
		if not occupation:
			raise GraphQLError("Invalid occupation, Please contact support.")
		else:
			return occupation
			
