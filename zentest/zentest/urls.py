from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from API import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'API.views.index', name='home'),
    url(r'^api/', csrf_exempt(views.HomeView.as_view()), name='api'),

    url(r'^admin/', include(admin.site.urls)),
)
