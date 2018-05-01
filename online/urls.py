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
    url(r'^reset-password/$',password_reset,name='reset_password'),
    url(r'^reset-passwrd/done/$',password_reset_done,name='password_reset_done'),
    url(r'^reset-passwrd/confirm/$',password_reset_confirm,name='password_reset_confirm'),
    url(r'^reset-passwrd/complete/$',password_reset_complete,name='password_reset_complete'),
    
    
]
