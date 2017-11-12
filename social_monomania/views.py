from django.shortcuts import render

def hello(request):
	return render(request, 'home.html')


def about(request):
	return render(request, 'about.html')
	
	
def faq(request):
	return render(request, 'faq.html')
	