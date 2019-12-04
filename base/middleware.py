# standard imports
import threading


class RequestMiddleware():
    thread_local = threading.local()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Save the user that makes the request
        self.thread_local.user = request.user
        response = self.get_response(request)
        return response
