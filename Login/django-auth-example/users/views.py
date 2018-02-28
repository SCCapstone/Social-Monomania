from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from .forms import RegisterForm


def register(request):
    # from get or post to request the next action
    # get request, next passes url such as /?next = value
    # post request, next pass the values, <input type ="hidden" name="next" value="{{next}}"/>
    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    # Only POST stands, means the user has register information
    if request.method == 'POST':
        # request.POST is a vector, that contains user register information
        # it is username, Password, re-entered password, and email
        form = RegisterForm(request.POST)

        #make sure the information are in correct form
        if form.is_valid():
            # if the information are legal, then save it to the database
            form.save()


            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:
        #if the request is not POST, means user is actually visiting the register page, just show the empty page of register form to the user
        form = RegisterForm()

    #form.py
    #if the user is visiting the register page, giving empty register form
    #if the user give illegal register information, then return an error message
    #register page redirect_to form.py and throght next value to pass this action
    return render(request, 'users/register.html', context={'form': form, 'next': redirect_to})


def index(request):
    return render(request, 'index.html')
