from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType
from api.models import UserProfile

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class Register(graphene.Mutation):
    """ Mutation to register a user """

    user = graphene.Field(UserType)    

    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, name, email, phone, password):
        user = get_user_model()(
            username=name,
            email=email,
        )
        user.set_password(password)
        user.save()

        UserProfile.objects.create(user=user, primary_phone=phone)

        return Register(user=user)


class UserMutation(graphene.ObjectType):
    register = Register.Field()

class UserQuery(graphene.ObjectType):
    me = graphene.Field(UserType)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user        