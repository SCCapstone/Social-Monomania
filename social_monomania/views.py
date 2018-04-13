from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from .forms import ContactForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate
from django.db import models
from utilities import basicHandler
from django.views import View
import json #added for export

try:
        import cStringIO as StringIO
except ImportError:
        import StringIO

from xlsxwriter.workbook import Workbook

def hello(request):
        if request.user.is_authenticated():
                return render(request, 'about.html')
        if not request.user.is_authenticated():
                return HttpResponseRedirect('online/login')

def search(request):
	return render(request, 'search.html')

def advSearch(request):
	return render(request, 'advSearch.html')


def help(request):
	return render(request, 'help.html')	
	
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
            subject = form.cleaned_data['subject']
            from_email = str(form.cleaned_data['from_email'])
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, [from_email], ['socialmonomania@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/thanks/')
    return render(request, "contact.html", {'form': form})

def graph(request):
        return render(request, 'graph.html')

def download(request):
        #create workbook
        output = StringIO.StringIO()
        
        #FORMATTING ------------------------------------------------------------------

        book = Workbook(output)
        sheet = book.add_worksheet('Reddit Results')
        twittersheet = book.add_worksheet('Twitter Results')

        #formatting for cells in excel
        titles_format = book.add_format({
                'bold': True,
                'border': 2,
                'font_color': 'white',
                'bg_color': '#9999FF',
                'valign': 'vcenter',
                'align': 'left',
                'font_size': 14})
        posts_format = book.add_format({
                'bold': 1,
                'font_size': 10,
                'align': 'left',
                'valign': 'top',
                'text_wrap': True})
        url_format = book.add_format({
                'bold': 1,
                'font_size': 10,
                'italic': True,
                'font_color': 'blue',
                'text_wrap': True,
                'align': 'left',
                'valign': 'top'})
        sheet.set_column('A:A', 35)
        sheet.set_column('B:B', 10)
        sheet.set_column('C:C', 50)
        twittersheet.set_column('A:A', 35)
        twittersheet.set_column('B:F', 15)
        twittersheet.set_column('G:K', 35)
        sheet.freeze_panes(1, 0)
        twittersheet.freeze_panes(1, 0)
        
        #------------------REDDIT------------------------------------------------

        #Spreadsheet titles for reddit sheet
        headerObjReddit = ['Post Title', 'Time', 'URL']
        redcol = 0
        for header in headerObjReddit:
                sheet.write(0,redcol, header, titles_format)
                redcol = redcol + 1
        
        redrow = 1
        redcol = 0
        #------------------REDDIT------------------------------------------------

        #Spreadsheet titles for reddit sheet
        headerObjReddit = ['Post Title', 'Time', 'URL']
        redcol = 0
        for header in headerObjReddit:
                sheet.write(0,redcol, header, titles_format)
                redcol = redcol + 1
        
        redrow = 1
        redcol = 0
        #error catching if Reddit isn't checked/returns 0 results
        if not redditVariable:
                sheet.write(1, 0, "No Reddit Data Found", posts_format)
        else:
                for entry in redditVariable:
                        sheet.write(redrow, redcol, entry, posts_format)
                        sheet.write(redrow, redcol+1, str(redditVariable[entry]['time']), posts_format)
                        sheet.write(redrow, redcol+2, redditVariable[entry]['url'], url_format)
                        redrow += 1

        #----------------------TWITTER------------------------------------------
        
        #titles in the sheet
        headerObj = ['Text', 'User', 'Date', 'Retweets', 'Favorited', 'Location', 'Link to Tweet', 'User Profile Link', '@Mention link', 'Media Link']
        twitcol = 0
        for header in headerObj:
                twittersheet.write(0,twitcol, header, titles_format)
                twitcol = twitcol + 1
        
        twitrow = 1
        twitcol = 0
        #error catching if Twitter box isn't checked/returns 0 results
        if not twitterVariable:
                twittersheet.write(1, 0, "No Twitter Data Found", posts_format)
        else:
                statusList = twitterVariable['statuses']
                mentionList = []
                mediaList = []
                for entry in statusList:
                        #text, user, date, retweets, favorited, geolocation, link
                        twittersheet.write(twitrow, twitcol, entry['text'], posts_format)
                        twittersheet.write(twitrow, twitcol+1, entry['user']['screen_name'], posts_format)
                        twittersheet.write(twitrow, twitcol+2, entry['created_at'], posts_format)
                        twittersheet.write(twitrow, twitcol+3, entry['retweet_count'], posts_format)
                        twittersheet.write(twitrow, twitcol+4, entry['favorite_count'], posts_format)
                        twittersheet.write(twitrow, twitcol+5, entry['user']['location'], posts_format)
                        twittersheet.write_url(twitrow, twitcol+6, 'https://www.twitter.com/statuses/'+str(entry['id']), url_format)
                        twittersheet.write_url(twitrow, twitcol+7, 'https://www.twitter.com/'+str(entry['user']['screen_name']), url_format)
                        #user mentions requires a bit more work.  The for-loop fills a list, and .join() is used in writing all the list elements
                        for mention in entry['entities']['user_mentions']:
                                mentionList.append('https://www.twitter.com/'+mention['screen_name']+'\n')
                        twittersheet.write_url(twitrow, twitcol+8, ''.join(mentionList), url_format)
                        #media links is similar to user mentions.  Was not possible to access
                        #with entry['extended_entities']['media']['media_url_https'], so had to
                        #work around it a bit.
                        if 'extended_entities' in entry:
                                for item in entry['extended_entities']['media']:
                                        mediaList.append(item['media_url_https']+'\n')
                        twittersheet.write_url(twitrow, twitcol+9, ''.join(mediaList), url_format)
        
                        #clear lists for next entry, go to next row to fill
                        mentionList[:] = []
                        mediaList[:] = []
                        twitrow += 1
        
                #------------------------------------------------------------------
        
        #Closing the workbook
        book.close()
        
        #construct response
        output.seek(0)
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=SM_Results.xlsx"

        return response
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=SM_Results.xlsx"

        return response

def results(request):

    if request.method == 'POST':
        print(request.POST)
        # print(request.POST['q'])
        # print(request.POST['boxes[]'])
        global searchQuery
        searchQuery = request.POST['q']
        redditReturn, twitterReturn = basicHandler.searchHandle(request.POST['q'], dict(request.POST)['boxes[]'])
        #reddit global variables
        global redditVariable
        redditVariable = redditReturn
        global redditVariable1
        #twitter global variables
        global twitterVariable
        twitterVariable = twitterReturn
        global twitterVariable1

    return render(request, 'results.html', {'redditReturn': redditReturn, 'twitterReturn': twitterReturn, 'searchQuery': searchQuery})

def advancedresults(request):

    if request.method == 'POST':
        print(request.POST)
        # print(request.POST['q'])
        # print(request.POST['boxes[]'])
        global searchQuery
        searchQuery = request.POST['q']
        redditReturn, twitterReturn = advancedHandler.searchHandle(request.POST['q'], dict(request.POST)['boxes[]'])
        #reddit global variables
        global redditVariable
        redditVariable = redditReturn
        global redditVariable1
        #twitter global variables
        global twitterVariable
        twitterVariable = twitterReturn
        global twitterVariable1
        
        

	return render(request, 'results.html', {'redditReturn': redditReturn, 'twitterReturn': twitterReturn, 'searchQuery': searchQuery})
	
