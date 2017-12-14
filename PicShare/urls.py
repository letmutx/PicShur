"""ImageSharing URL Configuration

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

from django.conf.urls import url

from PicShare import views

urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.account_logout, name='logout'),
    url(r'^picture/add$', views.add_picture, name='add_photo'),

    url(r'^picture/(?P<pk>\d+)/delete$', views.delete_picture, name='delete_photo'),
    url('^$', views.feed, name='feed'),

    url(r'^user/profile$', views.profile, name='profile'),
    url(r'^user/(?P<pk>\d+)/friend$', views.add_friend, name='add_friend'),
    url(r'^user/(?P<pk>\d+)/unfriend$', views.delete_friend, name='delete_friend'),
    url(r'^users/all$', views.users_list, name='all_users'),
]
