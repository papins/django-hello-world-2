from annoying.decorators import render_to
from django_hello_world.hello.models import UserInfo, Request
from django.shortcuts import get_object_or_404


@render_to('hello/home.html')
def home(request):
    user_info = get_object_or_404(UserInfo, pk=1)
    return {'user_info': user_info}


@render_to('hello/requests.html')
def requests(request):
    request_list = Request.objects.all()[:10]
    return {'request_list': request_list}
