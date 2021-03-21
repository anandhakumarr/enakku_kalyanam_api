import graphene
import graphql_jwt
from api.schemas.user import UserQuery, UserMutation
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
import graphene


class UserDataType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class ObtainJSONWebToken(graphql_jwt.ObtainJSONWebToken):
    user = graphene.Field(UserDataType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)

class Query(UserQuery, graphene.ObjectType):
    pass

class Mutation(UserMutation, graphene.ObjectType,):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)