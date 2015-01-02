from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from API import views

urlpatterns = patterns('',
    url(r'^$', 'API.views.index', name='home'),
    url(r'^test/new/$', 'API.views.createQuestionSet', name='new_question_set'),
    url(r'^test/(?P<slug>[\w-]+)/$', csrf_exempt(views.TestDetails.as_view()), name='test_details_view'),
    url(r'^test/(?P<slug>[\w-]+)/add/$', csrf_exempt(views.AddQuestion.as_view()), name='add_question'),
    url(r'^test/(?P<slug>[\w-]+)/start/$', csrf_exempt(views.LoadTestPage.as_view()), name='start_test'),
    url(r'^test/(?P<slug>[\w-]+)/load/$', csrf_exempt(views.LoadQuestions.as_view()), name='load_questions'),
    url(r'^admin/', include(admin.site.urls)),
)
