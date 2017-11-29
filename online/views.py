from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
from .models import User

# form
class UserForm(forms.Form): 
    username = forms.CharField(label='User Name',max_length=100)
    password = forms.CharField(label='Password',widget=forms.PasswordInput())


# register
def regist(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            # get data from base
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # add to cookie base
            User.objects.create(username= username,password=password)
            return HttpResponse('regist success!!')
    else:
        uf = UserForm()
    return render(req, 'regist.html',{'uf':uf})

# login
def login(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            # get password and username from user
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # comparing
            user = User.objects.filter(username__exact = username,password__exact = password)
            if user:
                # login succeed return to index page
                response = HttpResponseRedirect('/online/index/')
                # save username into cookie,resetting time 3600
                response.set_cookie('username',username,3600)
                return response
            else:
                # Failed to Login return to login
                return HttpResponseRedirect('/online/login/')
    else:
        uf = UserForm()
    return render(req, 'login.html',{'uf':uf})

# Log in Succeed
def index(req):
    username = req.COOKIES.get('username','')
    return render(req, 'index.html' ,{'username':username})

# Failed to Login
def logout(req):
    response = HttpResponse('logout !!')
    # clear cookie username
    response.delete_cookie('username')
    return response
