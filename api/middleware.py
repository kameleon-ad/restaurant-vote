from django.http import HttpRequest


class VersionControlRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):

        if not request.path_info.startswith('/api/def'):
            return self.get_response(request)

        version = request.headers.get('X-API-Version')
        if version is None:
            version = 2
        request.path_info = f'/api/v{ version }' + request.path_info[len('/api/def'):]
        response = self.get_response(request)
        return response
