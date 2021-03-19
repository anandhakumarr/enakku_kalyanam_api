import json
from django.utils.deprecation import MiddlewareMixin
from api.models import RequestLogger
from matrimony.schema import schema
from graphql import GraphQLError
from django.contrib.auth.models import User

class LogRestMiddleware(MiddlewareMixin):
    """Middleware to log every request/response.
    Is not triggered when the request/response is managed using the cache
    """

    @staticmethod
    def _log_request(request):
        """Log the request"""
        try:
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].replace('JWT ', '')
                verifyquery  =  ''' 
                                    mutation($token: String!) {
                                      verifyToken( token: $token)
                                      {
                                        payload
                                      }
                                    }        
                                '''
                response = schema.execute(verifyquery, variables={'token': token})
                try:
                    username = response.data['verifyToken']['payload']['username']
                    user = User.objects.filter(username=username).first()
                except:
                    raise GraphQLError("Operation Not Allowed, Please contact admin.")
                
            else:
                user = request.user
                print(user)

            method = str(getattr(request, 'method', '')).upper()
            request_path = str(getattr(request, 'path', ''))
            
            if request.content_type == 'application/json':
                post_params = json.loads(request.body.decode('utf-8'))
            else:
                post_params = {}
                for k,v in dict(request.POST).items():
                    if len(v) > 1:
                        post_params[k] = v
                    else:
                        post_params[k] = v[0]
            RequestLogger.objects.create(user=user, method=method, request_path=request_path, body=json.dumps(post_params))
            # print(user, method, request_path, post_params)
            # _logger.warning("req: (%s) [%s] %s %s", user, method, request_path, request.body)
        except Exception as e:
            print(e)

    def __call__(self, request):
        """Method call when the middleware is used in the `MIDDLEWARE` option in the settings (Django >= 1.10)"""
        if request.method != 'GET':
            self._log_request(request)
        response = self.get_response(request)
        # self._log_response(request, response)
        return response
