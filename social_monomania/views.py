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
                     'statuses_is_quote_status', 'retweeted_status_created_at',
                     'retweeted_status_id_str', 'retweeted_status_text',
                     'retweeted_status_entities_urls_url',
                     'retweeted_status_entities_urls_expanded_url',
                     'retweeted_entities_hashtags_text', 'retweeted_status_entities_user_mentions_screen_name',
                     'retweeted_status_entities_user_mentions_name', 'retweeted_status_entities_user_id_str',
                     'retweeted_status__entities__media__id_str', 'retweeted_status__entities__media__media_url',
                     'retweeted_status__entities__media__url', 'retweeted_status__entities__media__expanded_url',
                     'retweeted_status__entities__media__source_status_id_str',
                     'retweeted_status__entities__media__source_user_id_str',
                     'retweetedExtendedEntitiesMediaIDStr', 'retweetedExtendedEntitiesMediaMediaUrl',
                     'retweetedExtendedEntitiesMediaUrl', 'retweetedExtendedEntitiesMediaExpandedUrl',
                     'retweetedExtendedEntitiesMediaSourceStatusIDStr', 'retweetedExtendedEntitiesMediaSourceUserIDStr',
                     'retweetedMetadataISOLanguageCode', 'retweetedSource','retweetedInReplyToStatusIDStr',
                     'retweetedInReplyToUserIDStr', 'retweetedInReplyToScreenName',
                     'retweetedUserName', 'retweetedUserScreenName', 'retweetedUserLocation',
                     'retweetedUserDescription', 'retweetedUserURL', 'retweetedUserFollowersCount',
                     'retweetedUserFriendsCount', 'retweetedUserListedCount', 'retweetedUserCreatedAt',
                     'retweetedUserFavouritesCount', 'retweetedUserTimeZone', 'retweetedUserVerified',
                     'retweetedUserLang', 'retweetedUserProfileBackgroundImageURL',
                     'retweetedUserProfileImageURL', 'retweetedUserFollowing',
                     'retweetedGeo', 'retweetedCoordinates', 'retweetedPlace', 'retweetedIsQuoteStatus',
                     'retweetedRetweetCount', 'retweetedFavoriteCount', 'retweetedFavorited',
                     'retweetedRetweeted', 'retweetedPossiblySensitive', 'retweetedLang'
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

                #these are the lists created for entries that require lists.
                #these include information derived from the dictionary
                #nested in a list nested in the main dictionary.  In Twitter,
                #a user might link multiple media links (images, for example)
                #and in order to capture ALL of these links, they have to put into
                #a list.  And if there are multiple medias, that means there is
                #potential for multiple media IDs, Urls, Sources, etc.  This is the
                #reason for the large number of lists.
                mentionList = []
                mediaList = []
                following = []
                quotedMediaList = []
                quotedMediaIDList = []
                entitiesMediaExpandedUrlList = []
                entitiesMediaUrlList = []
                entitiesMediaMediaUrlList = []
                entitiesMediaIDstr = []
                retweetedStatusEntitiesUrlsUrl = []
                retweetedStatusEntitiesUrlsExpandedUrl = []
                retweetedEntitiesHashtags = []
                retweetedUserMentionsScreenNames = []
                retweetedUserMentionsNames = []
                retweetedUserMentionsIDstrs = []
                retweetedEntitiesMediaIDstr = []
                retweetedEntitiesMediaMediaUrl = []
                retweetedEntitiesMediaUrl = []
                retweetedEntitiesMediaExpUrl = []
                retweetedEntitiesMediaSourceStatusID = []
                retweetedEntitiesMediaSourceUserIDstr = []
                # started 4/26
                retweetedExtendedEntitiesMediaIDStr = []
                retweetedExtendedEntitiesMediaMediaUrl = []
                retweetedExtendedEntitiesMediaUrl = []
                retweetedExtendedEntitiesMediaExpandedUrl = []
                retweetedExtendedEntitiesMediaSourceStatusIDStr = []
                retweetedExtendedEntitiesMediaSourceUserIDStr = []
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

                        #START - quoted_status
                        
                        #this if-else checks if quoted_status, exists, then writes the data of the
                        #quoted status in the cell.  If quoted_status doesn't exist, it writes
                        #'DNE' in the cell for Does Not Exist

                        #----------NOTE-----------
                        #each of these if-statements below are necessary for error catching.  In some cases,
                        #the if statement is needed because of the way the json file is created.
                        #Sometimes there are dictionaries of lists, while sometimes there are additional
                        #lists of dictionaries nested in these parent dictionaries.  In each case,
                        #it might be different in the approach to extract the information for the
                        #excel field, but the technique in the if-statements and for-loops are
                        #consistent throughout this document.
                        #-------------------------
                        
                        if 'quoted_status' in entry:
                                #to make sure you get hits for search results that have a quoted status, search for
                                #'statuses' for twitter
                                #print "FOR TESTING YESYESYEYSEYEYESYS"
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
                                #this one row below with coordinates was throwing an error of 'Unsupported type <type 'dict'> in write()'
                                #commenting it out for now
                                #twittersheet.write(twitrow, twitcol+20, entry['quoted_status']['coordinates'], posts_format)
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
                                #UPDATE: as a workaround, the way to fix this is to treat it as a list. See below (line 274) how 'id_str' was
                                #fixed - it was giving me the same errors before.
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
                                        twittersheet.write(twitrow, twitcol+39, 'No media url', posts_format)                                
                                        twittersheet.write(twitrow, twitcol+40, 'No media url ID', posts_format)
                                        
                                if 'entities' in entry['quoted_status']:
                                        if 'media' in entry['quoted_status']['entities']:
                                                for item in entry['quoted_status']['entities']['media']:
                                                        entitiesMediaExpandedUrlList.append(item['expanded_url']+'\n')
                                                        entitiesMediaUrlList.append(item['url']+'\n')
                                                        entitiesMediaMediaUrlList.append(item['media_url']+'\n')
                                                        entitiesMediaIDstr.append(item['id_str']+'\n')
                                twittersheet.write_url(twitrow, twitcol+41, ''.join(entitiesMediaExpandedUrlList), url_format)
                                twittersheet.write_url(twitrow, twitcol+42, ''.join(entitiesMediaUrlList), url_format)
                                twittersheet.write_url(twitrow, twitcol+43, ''.join(entitiesMediaMediaUrlList), url_format)
                                twittersheet.write(twitrow, twitcol+44, ''.join(entitiesMediaIDstr), posts_format)
                                twittersheet.write(twitrow, twitcol+45, entry['quoted_status']['text'], posts_format)
                                twittersheet.write(twitrow, twitcol+46, entry['quoted_status']['id_str'], posts_format)
                                twittersheet.write(twitrow, twitcol+47, entry['quoted_status']['created_at'], posts_format)
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
                                twittersheet.write(twitrow, twitcol+41, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+42, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+43, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+44, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+45, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+46, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+47, 'DNE', posts_format)

                        #END - quoted_status

                        #is_quote_status' parent is simply [statuses]
                        twittersheet.write(twitrow, twitcol+48, bool(entry['is_quote_status']), posts_format)
                        
                        #START - retweeted status

                        if 'retweeted_status' in entry:
                                #print "(FOR TESTING) RETWEETED STATUS PRESENT"
                                twittersheet.write(twitrow, twitcol+49, entry['retweeted_status']['created_at'], posts_format)
                                twittersheet.write(twitrow, twitcol+50, entry['retweeted_status']['id_str'], posts_format)
                                twittersheet.write(twitrow, twitcol+51, entry['retweeted_status']['text'], posts_format)
                                for item in entry['retweeted_status']['entities']['urls']:
                                        retweetedStatusEntitiesUrlsUrl.append(item['url']+'\n')
                                        retweetedStatusEntitiesUrlsExpandedUrl.append(item['expanded_url']+'\n')
                                twittersheet.write_url(twitrow, twitcol+52, ''.join(retweetedStatusEntitiesUrlsUrl), url_format)
                                twittersheet.write_url(twitrow, twitcol+53, ''.join(retweetedStatusEntitiesUrlsExpandedUrl), url_format)
                                if 'entities' in entry['retweeted_status']:
                                        if 'hashtags' in entry['retweeted_status']['entities']:
                                                for item in entry['retweeted_status']['entities']['hashtags']:
                                                        retweetedEntitiesHashtags.append('#'+item['text']+'\n')
                                twittersheet.write(twitrow, twitcol+54, ''.join(retweetedEntitiesHashtags), posts_format)
                                if 'entities' in entry['retweeted_status']:
                                        if 'user_mentions' in entry['retweeted_status']['entities']:
                                                for item in entry['retweeted_status']['entities']['user_mentions']:
                                                        retweetedUserMentionsScreenNames.append('@'+item['screen_name']+'\n')
                                                        retweetedUserMentionsNames.append('@'+item['name']+'\n')
                                                        retweetedUserMentionsIDstrs.append('@'+item['id_str']+'\n') 
                                twittersheet.write(twitrow, twitcol+55, ''.join(retweetedUserMentionsScreenNames), posts_format)
                                twittersheet.write(twitrow, twitcol+56, ''.join(retweetedUserMentionsNames), posts_format)
                                twittersheet.write(twitrow, twitcol+57, ''.join(retweetedUserMentionsIDstrs), posts_format)
                                if 'entities' in entry['retweeted_status']:
                                        if 'media' in entry['retweeted_status']['entities']:
                                                for item in entry['retweeted_status']['entities']['media']:
                                                        retweetedEntitiesMediaIDstr.append(item['id_str']+'\n') 
                                                        retweetedEntitiesMediaMediaUrl.append(item['media_url']+'\n')
                                                        retweetedEntitiesMediaUrl.append(item['url']+'\n')
                                                        retweetedEntitiesMediaExpUrl.append(item['expanded_url']+'\n')
                                                        if 'source_status_id_str' in item:
                                                                retweetedEntitiesMediaSourceStatusID.append(item['source_status_id_str']+'\n')
                                                        if 'source_user_id_str' in item:
                                                                retweetedEntitiesMediaSourceUserIDstr.append(item['source_user_id_str']+'\n')
                                twittersheet.write(twitrow, twitcol+58, ''.join(retweetedEntitiesMediaIDstr), posts_format)
                                twittersheet.write_url(twitrow, twitcol+59, ''.join(retweetedEntitiesMediaMediaUrl), url_format)
                                twittersheet.write_url(twitrow, twitcol+60, ''.join(retweetedEntitiesMediaUrl), url_format)
                                twittersheet.write_url(twitrow, twitcol+61, ''.join(retweetedEntitiesMediaExpUrl), url_format)
                                twittersheet.write(twitrow, twitcol+62, ''.join(retweetedEntitiesMediaSourceStatusID), posts_format)
                                twittersheet.write(twitrow, twitcol+63, ''.join(retweetedEntitiesMediaSourceUserIDstr), posts_format)
                                #started here 4/26
                                if 'extended_entities' in entry['retweeted_status']:
                                        for item in entry['retweeted_status']['extended_entities']['media']:
                                                retweetedExtendedEntitiesMediaIDStr.append(item['id_str']+'\n')
                                                retweetedExtendedEntitiesMediaMediaUrl.append(item['media_url']+'\n')
                                                retweetedExtendedEntitiesMediaUrl.append(item['url']+'\n')
                                                retweetedExtendedEntitiesMediaExpandedUrl.append(item['expanded_url']+'\n')
                                                if 'source_status_id_str' in item:
                                                        retweetedExtendedEntitiesMediaSourceStatusIDStr.append(item['source_status_id_str']+'\n')
                                                if 'source_user_id_str' in item:
                                                        retweetedExtendedEntitiesMediaSourceUserIDStr.append(item['source_user_id_str']+'\n')
                                twittersheet.write(twitrow, twitcol+64, ''.join(retweetedExtendedEntitiesMediaIDStr), posts_format)
                                twittersheet.write_url(twitrow, twitcol+65, ''.join(retweetedExtendedEntitiesMediaMediaUrl), url_format)
                                twittersheet.write_url(twitrow, twitcol+66, ''.join(retweetedExtendedEntitiesMediaUrl), url_format)
                                twittersheet.write_url(twitrow, twitcol+67, ''.join(retweetedExtendedEntitiesMediaExpandedUrl), url_format)
                                twittersheet.write(twitrow, twitcol+68, ''.join(retweetedExtendedEntitiesMediaSourceStatusIDStr), posts_format)
                                twittersheet.write(twitrow, twitcol+69, ''.join(retweetedExtendedEntitiesMediaSourceUserIDStr), posts_format)
                                if 'metadata' in entry['retweeted_status']:
                                        twittersheet.write(twitrow, twitcol+70, entry['retweeted_status']['metadata']['iso_language_code'], posts_format)
                                twittersheet.write(twitrow, twitcol+71, entry['retweeted_status']['source'], posts_format)
                                twittersheet.write(twitrow, twitcol+72, entry['retweeted_status']['in_reply_to_status_id_str'], posts_format)
                                twittersheet.write(twitrow, twitcol+73, entry['retweeted_status']['in_reply_to_user_id_str'], posts_format)
                                twittersheet.write(twitrow, twitcol+74, entry['retweeted_status']['in_reply_to_screen_name'], posts_format)
                                twittersheet.write(twitrow, twitcol+75, entry['retweeted_status']['user']['name'], posts_format)
                                twittersheet.write(twitrow, twitcol+76, entry['retweeted_status']['user']['screen_name'], posts_format)
                                twittersheet.write(twitrow, twitcol+77, entry['retweeted_status']['user']['location'], posts_format)
                                twittersheet.write(twitrow, twitcol+78, entry['retweeted_status']['user']['description'], posts_format)
                                twittersheet.write_url(twitrow, twitcol+79, str(entry['retweeted_status']['user']['url']), url_format)
                                twittersheet.write(twitrow, twitcol+80, entry['retweeted_status']['user']['followers_count'], posts_format)
                                twittersheet.write(twitrow, twitcol+81, entry['retweeted_status']['user']['friends_count'], posts_format)
                                twittersheet.write(twitrow, twitcol+82, entry['retweeted_status']['user']['listed_count'], posts_format)
                                twittersheet.write(twitrow, twitcol+83, entry['retweeted_status']['user']['created_at'], posts_format)
                                twittersheet.write(twitrow, twitcol+84, entry['retweeted_status']['user']['favourites_count'], posts_format)
                                twittersheet.write(twitrow, twitcol+85, entry['retweeted_status']['user']['time_zone'], posts_format)
                                twittersheet.write(twitrow, twitcol+86, entry['retweeted_status']['user']['verified'], posts_format)
                                twittersheet.write(twitrow, twitcol+87, entry['retweeted_status']['user']['lang'], posts_format)
                                twittersheet.write_url(twitrow, twitcol+88, str(entry['retweeted_status']['user']['profile_background_image_url']), url_format)
                                twittersheet.write_url(twitrow, twitcol+89, str(entry['retweeted_status']['user']['profile_image_url']), url_format)
                                twittersheet.write(twitrow, twitcol+90, entry['retweeted_status']['user']['following'], posts_format)
                                twittersheet.write(twitrow, twitcol+91, entry['retweeted_status']['geo'], posts_format)
                                #coordinates is messing up, commenting out for now
                                #twittersheet.write(twitrow, twitcol+92, entry['retweeted_status']['coordinates'], posts_format)
                                #place requires this if/else statement and error catcher like it did before
                                if entry['retweeted_status']['place'] != None:
                                        if 'country' in entry['retweeted_status']['place']:
                                                twittersheet.write(twitrow, twitcol+93, entry['retweeted_status']['place']['country'], posts_format)
                                        else:
                                                twittersheet.write(twitrow, twitcol+93, 'No country listed', posts_format)
                                twittersheet.write(twitrow, twitcol+94, entry['retweeted_status']['is_quote_status'], posts_format)
                                twittersheet.write(twitrow, twitcol+95, entry['retweeted_status']['retweet_count'], posts_format)
                                twittersheet.write(twitrow, twitcol+96, entry['retweeted_status']['favorite_count'], posts_format)
                                twittersheet.write(twitrow, twitcol+97, entry['retweeted_status']['favorited'], posts_format)
                                twittersheet.write(twitrow, twitcol+98, entry['retweeted_status']['retweeted'], posts_format)
                                if 'possibly_sensitive' in ['retweeted_status']:
                                        twittersheet.write(twitrow, twitcol+99, entry['retweeted_status']['possibly_sensitive'], posts_format)
                                else:
                                        twittersheet.write(twitrow, twitcol+99, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+100, entry['retweeted_status']['lang'], posts_format)


                                
                                


                        else:
                                #this can be condensed later using a loop
                                twittersheet.write(twitrow, twitcol+49, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+50, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+51, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+52, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+53, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+54, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+55, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+56, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+57, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+58, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+59, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+60, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+61, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+62, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+63, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+64, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+65, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+66, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+67, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+68, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+69, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+70, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+71, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+72, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+73, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+74, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+75, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+76, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+77, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+78, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+79, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+80, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+81, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+82, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+83, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+84, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+85, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+86, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+87, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+88, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+89, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+90, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+91, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+92, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+93, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+94, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+95, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+96, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+97, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+98, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+99, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+100, 'DNE', posts_format)


                        #END - retweeted status
        
                        #clear lists for next entry, go to next row to fill
                        mentionList[:] = []
                        mediaList[:] = []
                        following[:] = []
                        quotedMediaList[:] = []
                        quotedMediaIDList[:] = []
                        entitiesMediaExpandedUrlList[:] = []
                        entitiesMediaUrlList[:] = []
                        entitiesMediaMediaUrlList[:] = []
                        entitiesMediaIDstr[:] = []
                        retweetedStatusEntitiesUrlsUrl[:] = []
                        retweetedStatusEntitiesUrlsExpandedUrl[:] = []
                        retweetedEntitiesHashtags[:] = []
                        retweetedUserMentionsScreenNames[:] = []
                        retweetedUserMentionsNames[:] = []
                        retweetedUserMentionsIDstrs[:] = []
                        retweetedEntitiesMediaIDstr[:] = []
                        retweetedEntitiesMediaMediaUrl[:] = []
                        retweetedEntitiesMediaUrl[:] = []
                        retweetedEntitiesMediaExpUrl[:] = []
                        retweetedEntitiesMediaSourceStatusID[:] = []
                        retweetedEntitiesMediaSourceUserIDstr[:] = []
                        retweetedExtendedEntitiesMediaIDStr = []
                        retweetedExtendedEntitiesMediaMediaUrl = []
                        retweetedExtendedEntitiesMediaUrl = []
                        retweetedExtendedEntitiesMediaExpandedUrl = []
                        retweetedExtendedEntitiesMediaSourceStatusIDStr = []
                        retweetedExtendedEntitiesMediaSourceUserIDStr = []

                        #go to next row
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
        if(request.POST['q2'] == ''):
            searchQuery = request.POST['q1']
        else:
            queryOne  = request.POST['q1']
            queryTwo  = request.POST['q2']
            booleanOp = request.POST['booleanOperator']
            searchQuery = queryOne + " " + booleanOp + " " + queryTwo
        
        twitterDate = request.POST['newestDate']

        subredditsDict = []

        try:
            subredditsDict = dict(request.POST)['subboxes[]']
        except Exception as e:
            print("Sub boxes empty")

        if(subredditsDict == []):
            subredditsDict.append(request.POST['searchCustomSub'])
            if(subredditsDict == [u'']):
                subredditsDict = ['news']
        else:
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
	
