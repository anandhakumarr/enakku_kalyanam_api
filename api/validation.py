from api.models import *

class Validation:

    def validate_hobby_category(category):
        if HobbyCategory.objects.filter(title=category):
            raise GraphQLError("Category already exists")
        

