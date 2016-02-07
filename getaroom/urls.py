"""getaroom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
import booker

from . import views

urlpatterns = [
    # getaroom.space/
    # redirects to booker app
	url(r'^$', views.home, name='home'),
    # /booker/
	url(r'^booker/', include('booker.urls')),
    # /admin_portal/

    # url(r'^admin_login/', booker.views.admin_login, name="admin_login"),
    # /admin/
    url(r'^admin/', admin.site.urls),
]
