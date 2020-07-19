import graphene
from graphene_django import DjangoObjectType
from api.models import *
from api.validation import *
from graphene import relay, ObjectType
from django.db.models import Q
import datetime
from graphql_jwt.decorators import login_required, staff_member_required



def get_wrapper_details(data_wrapper, qs, page, size, history=None):
    if page <= 1:
        skip = 0
        current_page = 1
    else:
        skip = (page - 1) * size
        current_page = page

    total_elements = qs.count()
    total_pages = int(total_elements / size) 
    total_pages += 1 if (total_elements % size) > 0 else 0

    
    if total_pages > current_page:
        has_next_page = True
    else:
        has_next_page = False

    if skip:
        qs = qs[skip:]
    if size:
        qs = qs[:size]

    number_of_elements = qs.count()

    keyword_args = {
        'results': qs,
        'total_elements': total_elements,
        'size': size,
        'total_pages': total_pages,
        'current_page': current_page,
        'has_next_page': has_next_page,
        'number_of_elements': number_of_elements,         
    }
    return data_wrapper(**keyword_args)


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


class ApiMutation(graphene.ObjectType):
    create_hobby_category = CreateHobbyCategory.Field()


class ApiQuery(graphene.ObjectType):

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

