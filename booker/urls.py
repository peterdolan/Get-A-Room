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
    url(r'^calendar/eventsfeed/(?P<room_name>.+)/$', views.eventsFeed, name='eventsfeed'),
    url(r'^profile/$', views.user_profile, name='profile'),
    url(r'^groupres/$', views.groupres, name='groupres'),
    url(r'^singleres/$', views.singleres, name='singleres'),
    url(r'^create_group/$', views.create_group, name='create_group'),
    url(r'^create_organization/$', views.create_organization, name='create_organization'),
    url(r'^delete_profile_info/$',views.delete_profile_info,name='delete_profile_info'),
    url(r'^groups/$',views.groups,name='groups'),
    url(r'^organizations/$',views.organizations,name='organizations'),
    url(r'^join_group_request/$',views.join_group_request,name='join_group_request'),
    url(r'^join_org/$',views.join_org,name='join_org'),
    url(r'^user/$',views.user,name='user'),
    url(r'^buildings/$',views.buildings,name='buildings'),
    url(r'^calendar/get_closest_reservation/$',views.get_closest_reservation,name='get_closest_reservation'),
    url(r'^settings/$',views.settings,name='settings'),
    url(r'^change_password/$',views.change_password,name='change_password'),
    url(r'^change_profile_picture/$',views.change_profile_picture,name='change_profile_picture'),
    url(r'^user_profiles/$',views.user_profiles,name='user_profiles'),
    url(r'^add_user_to_group/$',views.add_user_to_group,name='add_user_to_group/'),
    url(r'^add_group_admin/$',views.add_group_admin,name='add_group_admin/'),
    ]