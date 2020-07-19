import json
from django.utils.deprecation import MiddlewareMixin
from api.models import RequestLogger


class LogRestMiddleware(MiddlewareMixin):
    """Middleware to log every request/response.
    Is not triggered when the request/response is managed using the cache
    """

    @staticmethod
    def _log_request(request):
        """Log the request"""
        user = request.user.id
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

    def __call__(self, request):
        """Method call when the middleware is used in the `MIDDLEWARE` option in the settings (Django >= 1.10)"""
        if 'Authorization' in request.headers:
            self._log_request(request)
        response = self.get_response(request)
        # self._log_response(request, response)
        return response
