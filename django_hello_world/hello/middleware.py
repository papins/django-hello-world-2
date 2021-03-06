# from annoying.decorators import render_to
from django_hello_world.hello.models import Request
# from django.shortcuts import get_object_or_404


class RequestsLoggerMiddleware(object):
    def process_request(self, request):
        is_get = True if request.method == 'GET' else False
        r = Request.objects.create(path=request.path, is_get=is_get)
        r.save()
        return None
