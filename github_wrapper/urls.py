"""github_wrapper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from github_api import views
# from django.contrib.auth.views import (
#     login, logout, password_reset, password_reset_done, password_reset_confirm,
#     password_reset_complete
# )


urlpatterns = [
    # url(r'^login/$', login, {'template_name': 'accounts/login.html'}, name='login'),
    # url(r'^logout/$', logout, {'template_name': 'accounts/logout.html'}, name='logout'),
    url(r'^register/$', views.sign_up, name='register'),
    url('admin/', admin.site.urls)
]
