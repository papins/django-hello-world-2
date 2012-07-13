from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'django_hello_world.hello.views.home', name='home'),
    url(r'^requests/$', 'django_hello_world.hello.views.requests', name='requests'),
    url(r'^edit/$', 'django_hello_world.hello.views.edit_data', name='edit'),

    # admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'hello/login.html'}),
)

# Serve MEDIA files via developer server (DEBUG = True)
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
