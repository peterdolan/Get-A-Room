from django.conf.urls import include, url

from . import views

app_name = 'booker'
urlpatterns = [
    # ex: /booker/
    url(r'^$', views.index, name='index'),
    url(r'^confirm/(?P<name>[a-zA-Z0-9]+)/$', views.confirm, name='confirm'),
    ]
