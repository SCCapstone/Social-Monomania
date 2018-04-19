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
from utilities import advancedHandler
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
        headerObj = ['Text', 'User', 'Date', 'Retweets', 'Favorited',
                     'Location', 'Link to Tweet', 'User Profile Link',
                     '@Mention link', 'Media Link', 'lang','retweeted',
                     'favorited', 'quoted_status_lang', 'quoted_status_retweeted',
                     'quoted_status_favorited', 'quoted_status_favorite_count',
                     'quoted_status_retweet_count', 'quoted_status_is_quote_status',
                     'quoted_status_place', 'quoted_status_coordinates',
                     'quoted_status_geo', 'quoted_status_user_created_at',
                     'quoted_status_user_following', 'quoted_status_user_profile_img_url',
                     'quoted_status_user_profile_background_image_url',
                     'quoted_status_user_lang', 'quoted_status_user_time_zone',
                     'quoted_status_favourites_count', 'quoted_status_listed_count',
                     'quoted_status_friends_count', 'quoted_status_followers_count',
                     'quoted_status__user__entities__url__urls__expanded_url spreadsheet',
                     'quoted_status_user_url', 'quoted_status_user_description',
                     'quoted_status_user_location',
                     'quoted_status_user_screen name', 'quoted_status_user_name',
                     'quoted_status_in_reply_to_screen_name',
                     'quoted_status_extended_entities_media_media_url',
                     'quoted_status_extended_entities_media_id_str',
                     'quoted_status_entities_media_expanded_url',
                     'quoted_status_entities_media_id_str', 'quoted_status_entities_media_url',
                     'quoted_status_entities_media_id_str', 'quoted_status_text',
                     'quoted_status_id_str', 'quoted_status_created_at',
                     'quoted_status_id_str'
                     ]
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
                following = []
                quotedMediaList = []
                quotedMediaIDList = []
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
                        twittersheet.write(twitrow, twitcol+10, entry['lang'], posts_format)
                        twittersheet.write(twitrow, twitcol+11, str(entry['retweeted']), posts_format)
                        twittersheet.write(twitrow, twitcol+12, str(entry['favorited']), posts_format)
                        #this if-else checks if quoted_status, exists, then writes the data of the
                        #quoted status in the cell.  If quoted_status doesn't exist, it writes
                        #'DNE' in the cell for Does Not Exist
                        if 'quoted_status' in entry:
                                #to make sure you get hits for search results that have a quoted status, search for
                                #'statuses' for twitter
                                print "FOR TESTING YESYESYEYSEYEYESYS"
                                twittersheet.write(twitrow, twitcol+13, entry['quoted_status']['lang'], posts_format)
                                twittersheet.write(twitrow, twitcol+14, str(entry['quoted_status']['retweeted']), posts_format)
                                twittersheet.write(twitrow, twitcol+15, str(entry['quoted_status']['favorited']), posts_format)
                                twittersheet.write(twitrow, twitcol+16, entry['quoted_status']['favorite_count'], posts_format)
                                twittersheet.write(twitrow, twitcol+17, entry['quoted_status']['retweet_count'], posts_format)
                                twittersheet.write(twitrow, twitcol+18, str(entry['quoted_status']['is_quote_status']), posts_format)
                                #['quoted_status']['place'] was throwing errors if I didn't use this double if-statement
                                if entry['quoted_status']['place'] != None:
                                        if 'country' in entry['quoted_status']['place']:
                                                twittersheet.write(twitrow, twitcol+19, entry['quoted_status']['place']['country'], posts_format)
                                        else:
                                                twittersheet.write(twitrow, twitcol+19, 'No country listed', posts_format)
                                twittersheet.write(twitrow, twitcol+20, entry['quoted_status']['coordinates'], posts_format)
                                twittersheet.write(twitrow, twitcol+21, entry['quoted_status']['geo'], posts_format)
                                twittersheet.write(twitrow, twitcol+22, entry['quoted_status']['user']['created_at'], posts_format)
                                twittersheet.write(twitrow, twitcol+23, bool(entry['quoted_status']['user']['following']), posts_format)
                                twittersheet.write_url(twitrow, twitcol+24, entry['quoted_status']['user']['profile_image_url'], url_format)
                                #background image required this error catching to function
                                if entry['quoted_status']['user']['profile_background_image_url'] != None:
                                        twittersheet.write_url(twitrow, twitcol+25, entry['quoted_status']['user']['profile_background_image_url'], url_format)
                                else:
                                        twittersheet.write(twitrow, twitcol+25, 'No background image url', posts_format)   
                                twittersheet.write(twitrow, twitcol+26, entry['quoted_status']['user']['lang'], posts_format)
                                twittersheet.write(twitrow, twitcol+27, entry['quoted_status']['user']['time_zone'], posts_format)
                                twittersheet.write(twitrow, twitcol+28, entry['quoted_status']['user']['favourites_count'], posts_format)
                                twittersheet.write(twitrow, twitcol+29, entry['quoted_status']['user']['listed_count'], posts_format)
                                twittersheet.write(twitrow, twitcol+30, entry['quoted_status']['user']['friends_count'], posts_format)
                                twittersheet.write(twitrow, twitcol+31, entry['quoted_status']['user']['followers_count'], posts_format)
                                #skipping statuses__quoted_status__user__entities__url__urls__expanded_url for now, twitcol is 32
                                #if error is list indices must be integers not strings, it means that within the dictionary,
                                #there is a list you must access.  Haven't found the best way to do this
                                twittersheet.write_url(twitrow, twitcol+33, str(entry['quoted_status']['user']['url']), url_format)
                                twittersheet.write(twitrow, twitcol+34, entry['quoted_status']['user']['description'], posts_format)
                                twittersheet.write(twitrow, twitcol+35, entry['quoted_status']['user']['location'], posts_format)
                                twittersheet.write(twitrow, twitcol+36, entry['quoted_status']['user']['screen_name'], posts_format)
                                twittersheet.write(twitrow, twitcol+37, entry['quoted_status']['user']['name'], posts_format)
                                twittersheet.write(twitrow, twitcol+38, entry['quoted_status']['in_reply_to_screen_name'], posts_format)
                                if 'extended_entities' in entry['quoted_status']:
                                        for item in entry['quoted_status']['extended_entities']['media']:
                                                quotedMediaList.append(item['media_url']+'\n')
                                                quotedMediaIDList.append(item['id_str']+'\n')
                                        twittersheet.write_url(twitrow, twitcol+39, ''.join(quotedMediaList), url_format)                                
                                        twittersheet.write_url(twitrow, twitcol+40, ''.join(quotedMediaIDList), url_format)
                                else: 
                                        twittersheet.write_url(twitrow, twitcol+39, 'No media url', url_format)                                
                                        twittersheet.write_url(twitrow, twitcol+40, 'No media url ID', url_format)
                                
                                
                        else:
                                #could potentially make a loop out of this (after finishing fields) to condense code
                                twittersheet.write(twitrow, twitcol+13, 'DNE', posts_format)                                
                                twittersheet.write(twitrow, twitcol+14, 'DNE', posts_format)                                
                                twittersheet.write(twitrow, twitcol+15, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+16, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+17, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+18, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+19, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+20, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+21, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+22, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+23, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+24, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+25, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+26, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+27, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+28, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+29, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+30, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+31, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+32, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+33, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+34, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+35, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+36, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+38, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+39, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+40, 'DNE', posts_format)
        
                        #clear lists for next entry, go to next row to fill
                        mentionList[:] = []
                        mediaList[:] = []
                        following[:] = []
                        quotedMediaList[:] = []
                        quotedMediaIDList[:] = []
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
        queryOne  = request.POST['q1']
        queryTwo  = request.POST['q2']
        booleanOp = request.POST['booleanOperator']
        searchQuery = queryOne + " " + booleanOp + " " + queryTwo
        
        twitterDate = request.POST['newestDate']

        subredditsDict = dict(request.POST)['subboxes[]']
        subredditsDict.append(request.POST['searchCustomSub'])
        redditReturn, twitterReturn = advancedHandler.searchHandle(searchQuery, dict(request.POST)['boxes[]'], subredditsDict, twitterDate)
        #reddit global variables
        global redditVariable
        redditVariable = redditReturn
        global redditVariable1
        #twitter global variables
        global twitterVariable
        twitterVariable = twitterReturn
        global twitterVariable1
        
        

	return render(request, 'results.html', {'redditReturn': redditReturn, 'twitterReturn': twitterReturn, 'searchQuery': searchQuery})
	
