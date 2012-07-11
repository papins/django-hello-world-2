from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django_hello_world.hello.models import UserInfo, Request
from django.shortcuts import get_object_or_404, redirect
from django import forms
from django.forms.widgets import FileInput, DateInput
import settings
from widgets import CalendarWidget


@render_to('hello/home.html')
def home(request):
    user_info = get_object_or_404(UserInfo, pk=1)
    return {'user_info': user_info}


@render_to('hello/requests.html')
def requests(request):
    request_list = Request.objects.all().order_by('-pk')[:10]
    return {'request_list': request_list}


class EditDataForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=CalendarWidget(
        params="'dateFormat':'yy-mm-dd'"))
    photo = forms.ImageField(widget=FileInput())

    class Meta:
        model = UserInfo


@login_required
@render_to('hello/edit.html')
def edit_data(request):
    user_info = get_object_or_404(UserInfo, pk=1)
    form = EditDataForm(request.POST or None, request.FILES or None,
                        instance=user_info)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('home')

    return {'form': form}
