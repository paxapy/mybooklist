__author__ = 'pa'

from django.conf.urls import patterns, url

from polls import views


urlpatterns = patterns(
    '',
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.Detail.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/results/$', views.Results.as_view(), name='results'),
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)
