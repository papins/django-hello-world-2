from annoying.decorators import render_to
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django_hello_world.hello.models import UserInfo, Request
from django.shortcuts import get_object_or_404, redirect
from django import forms
from django.forms.widgets import FileInput, DateInput
from django.http import HttpResponse
import settings
from widgets import CalendarWidget
from lazy_encoder import LazyEncoder

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
def edit_data(request):
    user_info = get_object_or_404(UserInfo, pk=1)
    form = EditDataForm(request.POST or None, request.FILES or None,
                        instance=user_info)

    if request.method == 'POST':
        # pause for testing
        # import time
        # time.sleep(3)
        if request.is_ajax() or 'is_ajax' in request.POST:
            valid = form.is_valid()
            data = {
                'valid': valid,
            }

            if not valid:
                if request.POST.getlist('fields'):
                    fields = request.POST.getlist('fields') + ['__all__']
                    errors = dict([(key, val) for key, val in form.errors.iteritems() if key in fields])
                else:
                    errors = form.errors
                final_errors = {}
                for key, val in errors.iteritems():
                    if key == '__all__':
                        final_errors['__all__'] = val
                    # elif not isinstance(form.fields[key], forms.FileField):
                    else:
                        html_id = form.fields[key].widget.attrs.get('id') or form[key].auto_id
                        html_id = form.fields[key].widget.id_for_label(html_id)
                        final_errors[html_id] = val
                data['errors'] = final_errors
            else:
                item = form.save()
                data['img_url'] = item.photo.url

            json_serializer = LazyEncoder()
            return HttpResponse(json_serializer.encode(data), mimetype='text/html')
            # return HttpResponse("ok")
        else:
            if form.is_valid():
                form.save()
                return redirect('home')
            else:
                pass

    return direct_to_template(
        request,
        template="hello/edit.html",
        extra_context = {
            'form': form,
        }
    )
