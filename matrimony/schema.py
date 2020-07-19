import graphene
import graphql_jwt
from api.schema import ApiQuery,  ApiMutation
from api.users.schema import UserQuery,  UserMutation
from api.matching.schema import MatchingMutation, MatchingQuery

class Mutation(UserMutation, ApiMutation, MatchingMutation, graphene.ObjectType,):
	token_auth = graphql_jwt.ObtainJSONWebToken.Field()
	verify_token = graphql_jwt.Verify.Field()
	refresh_token = graphql_jwt.Refresh.Field()	

class Query(UserQuery, ApiQuery, MatchingQuery, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

