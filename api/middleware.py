from django.shortcuts import redirect


class VersionControlRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path_info.startswith('/api/def'):
            request.path_info = '/api/v2' + request.path_info[len('/api/def'):]

        response = self.get_response(request)
        return response
