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
        form = ContactForm()
        if request.method == 'POST':
        	form = form_class(data=request.POST)
        if form.is_valid():
            subject = request.POST.get(
                'subject'
            , '')
            from_email = request.POST.get(
                'from_email'
            , '')
            message = request.POST.get('message', '')

            # Email the profile with the 
            # contact information
            email = EmailMessage(
                "New contact form submission",
                content,
                "Your website" +'',
                ['youremail@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return redirect('contact')

    return render(request, 'contact.html', {
        'form': form,
    })
def thanks(request):
    return HttpResponse('Thank you for your message.')
    
    