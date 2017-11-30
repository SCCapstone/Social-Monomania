from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm


def hello(request):
	return render(request, 'home.html')


def about(request):
	return render(request, 'about.html')
	
	
def faq(request):
	return render(request, 'faq.html')
	
	
def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_email(subject, message, from_email, ['socialmonomania@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('thanks')
    return render(request, "contact.html", {'form': form})

def thanks(request):
    return HttpResponse('Thank you for your message.')