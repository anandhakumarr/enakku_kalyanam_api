import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required, staff_member_required
from graphene import ObjectType
from api.models import HobbyCategory
from api.schemas.validation import Validation
from django.db.models import Q
import datetime


class HobbyCategoryType(DjangoObjectType):
    class Meta:
        model = HobbyCategory

class HobbyCategoryWrapper(ObjectType):
    results = graphene.List(HobbyCategoryType)
    total_elements = graphene.Int()
    number_of_elements = graphene.Int()
    size = graphene.Int()
    total_pages = graphene.Int()
    current_page = graphene.Int()
    has_next_page = graphene.Boolean()


class CreateHobbyCategory(graphene.Mutation):
    title = graphene.String()

    hobby_category = graphene.Field(HobbyCategoryType)

    class Arguments:
        title = graphene.String()

    @staff_member_required
    def mutate(self, info, title):

        # Validation
        Validation.validate_hobby_category(title)    

        category = HobbyCategory.objects.create(title=title)
        return CreateHobbyCategory(hobby_category=category)



class HobbyMutation(graphene.ObjectType):
    create_hobby_category = CreateHobbyCategory.Field()


class HobbyQuery(graphene.ObjectType):

    hobby_category = graphene.Field(
                HobbyCategoryWrapper,
                title=graphene.String(),
                size=graphene.Int(),
                page=graphene.Int())

    @login_required
    def resolve_hobby_category(self, info, title=None, size=100, page=1, **kwargs):
        qs = HobbyCategory.objects.all()
        query_filter = {}
        if title is not None:
            query_filter['title'] = title
        if query_filter:
            qs = qs.filter(**query_filter)
        return get_wrapper_details(HobbyCategoryWrapper, qs, page, size) 
