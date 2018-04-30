from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib import auth
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from django.db import models

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .forms import SignUpForm


# form
class UserForm(forms.Form): 
    username = forms.CharField(label='User Name',max_length=100)
    password = forms.CharField(label='Password',widget=forms.PasswordInput())


def registered(request):
	return render(request, 'registered.html')

# register
def regist(req):
    if req.method == 'POST':
        uf = SignUpForm(req.POST)
        if uf.is_valid():
            # get data from base
		form.save()
		username = form.cleaned_data.get('username')
		raw_password = form.cleaned_data.get('password1')
		user = authenticate(username=username, password=raw_password)
		login(req, user)
		return HttpResponseRedirect('/online/registered')
	else:
		form = SignUpForm()
		return render(req, 'regist.html', {'uf': uf})
	
            #username = uf.cleaned_data['username']
            #password = uf.cleaned_data['password']
            #if User.objects.filter(username=uf.cleaned_data['username']).exists():
             #   return HttpResponseRedirect('../regist')
            # add to cookie base
            #user = User.objects.create_user(username=username,password=password)
            #user.save()
            #return HttpResponseRedirect('/online/registered/')
    #else:
     #   uf = SignUpForm()
   # return render(req, 'regist.html',{'uf':uf})

# login
def login(req):
    if req.user.is_authenticated():
            return HttpResponseRedirect('../logout')
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            # get password and username from user
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # comparing
            # user = User.objects.filter(username__exact = username,password__exact = password)
            user = authenticate(username=username,password=password)
        try:    
            if user is not None:
                # login succeed return to index page
                auth_login(req,user)
                response = HttpResponseRedirect('/online/index/')
                # save username into cookie,resetting time 3600
                response.set_cookie('username',username,3600)
                return response
            else:
                # Failed to Login return to login
                return HttpResponseRedirect('/online/login/')
        except:
            return HttpResponseRedirect('/online/login/')

        '''
        try:    
            if user:
                # login succeed return to index page
                response = HttpResponseRedirect('/online/index/')
                # save username into cookie,resetting time 3600
                response.set_cookie('username',username,3600)
                return response
            else:
                # Failed to Login return to login
                return HttpResponseRedirect('/online/login/')
        except:
            return HttpResponseRedirect('/online/login/')
        '''

    else:
        uf = UserForm()
    return render(req, 'login.html',{'uf':uf})

# Log in Succeed
def index(req):
    username = req.COOKIES.get('username','')
    return render(req, 'index.html' ,{'username':username})

# Logout
def logout(req):
    auth.logout(req)
    username = req.COOKIES.get('username','')
    response = HttpResponseRedirect('../loggedout', username)
    # clear cookie username
    response.delete_cookie('username')
    return response
# Logged Out
def loggedout(req):
    return render(req, 'loggedout.html')

# change passsword
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })
