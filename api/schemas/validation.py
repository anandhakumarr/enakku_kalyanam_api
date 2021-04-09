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

