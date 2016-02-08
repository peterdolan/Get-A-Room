from django.conf.urls import include, url

from . import views

app_name = 'booker'
urlpatterns = [
    # ex: /booker/
    url(r'^$', views.index, name='index'),
    url(r'^confirm/$', views.confirm, name='confirm'),
    ]
