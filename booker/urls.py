from django.conf.urls import include, url

from . import views

app_name = 'booker'
urlpatterns = [
    # ex: /booker/
    url(r'^$', views.index, name='index'),
    url(r'^post_reservation/$', views.post_reservation, name='post_reservation'),
    url(r'^confirm/$', views.confirm, name='confirm'),
    url(r'^admin_dashboard/$', views.admin_dashboard, name='admin_dashboard'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^calendar/$', views.calendar_view, name='calendar'),
    url(r'^calendar/eventsfeed/(?P<building_name>.+)/$', views.eventsFeed, name='eventsfeed'),
    url(r'^profile/$', views.user_profile, name='profile'),
    url(r'^groupres/$', views.groupres, name='groupres'),
    url(r'^singleres/$', views.singleres, name='singleres'),
    url(r'^create_group/$', views.create_group, name='create_group'),
    url(r'^delete_profile_info/$',views.delete_profile_info,name='delete_profile_info'),
    url(r'^groups/$',views.groups,name='groups'),
    url(r'^organizations/$',views.organizations,name='organizations'),
    url(r'^join_group/$',views.join_group,name='join_group'),
    url(r'^join_org/$',views.join_org,name='join_org'),
    url(r'^user/$',views.user,name='user')
    ]
