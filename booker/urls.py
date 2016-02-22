from django.conf.urls import include, url

from . import views

app_name = 'booker'
urlpatterns = [
    # ex: /booker/
    url(r'^$', views.index, name='index'),
    url(r'^confirm/$', views.confirm, name='confirm'),
    url(r'^admin_dashboard/$', views.admin_dashboard, name='admin_dashboard'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^profile/$', views.user_profile, name='profile'),
    url(r'^create-group/$', views.create_group, name='create_group'),
    ]
