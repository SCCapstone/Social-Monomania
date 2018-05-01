from django.conf.urls import include , url
from online import views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^regist/$', views.regist, name='regist'),
    url(r'^index/$', views.index, name='index'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^loggedout/$', views.loggedout, name='loggedout'),
    url(r'^registered/$', views.registered, name='registered'),
    url(r'^password/$', views.change_password, name='change_password'),
    
    
    
    
]
