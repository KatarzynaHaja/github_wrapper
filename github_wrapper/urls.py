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
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # url(r'^login/$', login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'home/repos', views.HomeView.as_view(), name='repos'),

    url(r'^login/$', LoginView.as_view(), {'template_name': 'login.html', 'next_page':'repos'}, name='login'),
    url(r'^logout/$', LogoutView.as_view(), {'next_page': 'login'}, name='logout'),
    url(r'^register/$', views.sign_up, name='register'),
    url('admin/', admin.site.urls),
    url('add_new_repo', views.add_new_repo, name='add_new_repo'),
    # url('add_new_issue', views.add_new_issue, name='add_new_issue'),
    url(r'repos/home/(?P<pk>\d+)/add_issue/', views.add_new_issue, name='add_new_issue'),
    url(r'(?P<pk>\d+)/', views.get_repo_details, name='details')
]
