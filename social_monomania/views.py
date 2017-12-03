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
	
def thanks(request):
	return render(request, 'thanks.html')
	
	
def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['from_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            confirmation = 'We have received your report, and will review it shortly. Thank you!\n\nThe Social Monomania Team'
            try:
            	fullemail = message + "\n" + "\nFrom:\n" + email
                send_mail(subject, fullemail, [email], ['socialmonomania@gmail.com'])
                send_mail('Report Confirmation', confirmation, 'socialmonomania@gmail.com', [email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/thanks/')
    return render(request, "contact.html", {'form': form})
