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
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'home', views.HomeView.as_view(), name='Repo'),
    url(r'^login/$', LoginView.as_view(), {'template_name': 'login.html', 'next_page':'Repo'}, name='login'),
    url(r'^logout/$', LogoutView.as_view(), {'next_page': 'login'}, name='logout'),
    url(r'^register/$', views.sign_up, name='register'),
    url('admin/', admin.site.urls),
    url('add_new_repo', views.add_new_repo, name='add_new_repo'),
    url(r'repo/(?P<pk>\d+)/scrum_board/', views.scrum_board, name='scrum_board'),
    url(r'repo/(?P<pk>\d+)/add_issue/', views.add_new_issue, name='add_new_issue'),
    url(r'scrum_board/(?P<id>\d+)/details/', views.get_issue_details, name='issue_details'),
    url(r'add_personal_token', views.add_personal_token , name='add_personal_token'),
    url(r'refresh_data/(?P<pk>\d+)/', views.refresh_data, name='refresh_data'),
    url(r'remove_repo/(?P<pk>\d+)/', views.remove_repo, name='remove_repo'),
    url(r'update_token', views.update_personal_token, name='update_token')

]
