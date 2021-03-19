import graphene
import graphql_jwt
from api.schemas.user import UserQuery, UserMutation

class Query(UserQuery, graphene.ObjectType):
    pass

class Mutation(UserMutation, graphene.ObjectType,):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)