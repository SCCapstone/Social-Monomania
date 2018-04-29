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
        twittersheet.set_column('B:EQ', 15)
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
        
        #titles in the sheet.  There will be blank columns to be used for
        #Microsoft Azure Machine Learning sentiment analysis
        headerObj = ['CreatedAt', #1
                     'ID', #2
                     'Text', #3
                     '', #left blank for sentiment analysis field 4
                     '', #left blank for sentiment analysis field 5
                     'Geo', #6
                     'Coordinates', #7
                     'Place', #8
                     'Contributors', #9
                     'RetweetCount', #10
                     'FavoriteCount', #11
                     'Favorited', #12
                     'Retweete?', #13
                     'PossiblySensitive', #14
                     'Language', #15
                     'IsQuoteStatus', #16
                     'InReplyToStatusID', #17
                     'InReplyToUserID', #18
                     'InReplyToScreenName', #19
                     'UserID', #20
                     'UserScreenName', #21
                     'UserLocation', #22
                     'UserDescription', #23
                     'UserURL', #24
                     'UserEntitiesUrl_Urls_Url', #25
                     'UserEntitiesUrl_Urls_Expanded_Url', #26
                     'UserProtected', #27
                     'UserFollowersCount', #28
                     'UserFriendsCount', #29
                     'UserListedCount', #30
                     'UserCreatedAt', #31
                     'UserFavouritesCount', #32
                     'UserTimeZone', #33
                     'UserVerified', #34
                     'UserLang', #35
                     'UserContributorsEnabled', #36
                     'UserProfileBackgroundImageUrl', #37
                     'UserProfileImageUrl', #38
                     'UserProfileImageUrlHttps', #39
                     'UserProfileBbannerUrl', #40
                     'UserFollowing', #41
                     'HashtagsText', #42
                     'UserMentionsScreenName', #43
                     'UserMentionsName', #44
                     'UserMentionsID', #45
                     'MediaID', #46
                     'MediaUrl', #47
                     'MediaSourceUserID', #48
                     'ExtendedMediaUrl', #49
                     'ExtendedMediaSourceStatusID', #50
                     'ExtendedMediaSourceUserID', #51
                     'EntitiesUrl', #52
                     'RetweetedCreatedAt', #53
                     'RetweetedID', #54
                     'RetweetedText', #55
                     '', #left blank for sentiment analysis field 56
                     '', #left blank for sentiment analysis field 57
                     'RetweetedUrl', #58
                     'RetweetedUserName', #59
                     'RetweetedUserScreenName', #60
                     'RetweetedUserLocation', #61
                     'RetweetedUserDescription', #62
                     'RetweetedUserUrl', #63
                     'RetweetedUserUrlsUrl', #64
                     'RetweetedUserExpandedUrl', #65
                     'RetweetedUserFollowersCount', #66
                     'RetweetedUserFriendsCount', #67
                     'RetweetedUserListedCount', #68
                     'RetweetedUserCreatedAt', #69
                     'RetweetedUserFavouritesCount', #70
                     'RetweetedUserTimeZone', #71
                     'RetweetedUserVerified', #72
                     'RetweetedUserLang', #73
                     'RetweetedUserProfileBackgroundImageUrl', #74
                     'RetweetedUserProfileImageUrl', #75
                     'RetweetedUserFollowing', #76
                     'RetweetedGeo', #77
                     'RetweetedCoordinates', #78
                     'RetweetedPlace', #79
                     'RetweetedIsQuoteStatus', #80
                     'RetweetedRetweetCount', #81
                     'RetweetedFavoriteCount', #82
                     'RetweetedFavorited', #83
                     'RetweetedRetweeted', #84
                     'RetweetedPossiblySensitive', #85
                     'RetweetedLang', #86
                     'RetweetedExpandedUrl', #87
                     'RetweetedHashtagsText', #88
                     'RetweetedUserMentionsScreenName', #89
                     'RetweetedUserMentionsName', #90
                     'RetweetedUserMentionsID', #91
                     'RetweetedMediaID', #92
                     'RetweetedMediaMediaUrl', #93
                     'RetweetedMediaUrl', #94
                     'RetweetedMediaExpandedUrl', #95
                     'RetweetedMediaSourceStatusID', #96
                     'RetweetedMediaSourceUserID', #97
                     'RetweetedMediaID', #98
                     'RetweetedMediaMediaUrl', #99
                     'RetweetedMediaUrl', #100
                     'RetweetedMediaExpandedUrl', #101
                     'RetweetedMediaSourceStatusID', #102
                     'RetweetedMediaSourceUserID', #103
                     'RetweetedISOLanguageCode', #104
                     'RetweetedSource', #105
                     'RetweetedInReplyToStatusID', #106
                     'RetweetedInReplyToUserID', #107
                     'RetweetedInReplyToScreen_name', #108
                     'QuotedCreatedAt', #109
                     'QuotedID', #110
                     'QuotedText', #111
                     '', #left blank for sentiment analysis field 112
                     '', #left blank for sentiment analysis field 113
                     'QuotedGeo', #114
                     'QuotedCoordinates', #115
                     'QuotedPlace', #place is it's own dictionary. I will pull data from key 'country' from place dict  116
                     'QuotedIsQuoteStatus', #117
                     'QuotedRetweetCount', #118
                     'QuotedFavoriteCount', #119
                     'QuotedFavorited', #120
                     'QuotedRetweeted', #121
                     'QuotedPossiblySensitive', #122
                     'QuotedLangugage', #123
                     'QuotedUserName', #124
                     'QuotedUserScreenName', #125
                     'QuotedUserLocation', #126
                     'QuotedUserDescription', #127
                     'QuotedUserUrl', #128
                     'QuotedUserUrlsUrl', #129
                     'QuotedUserExpandedUrl', #130
                     'QuotedUserFollowersCount', #131
                     'QuotedUserFriendsCount', #132
                     'QuotedUserListedCount', #133
                     'QuotedUserCreatedAt', #134
                     'QuotedUserFavouritesCount', #135
                     'QuotedUserTimeZone', #136
                     'QuotedUserLang', #137
                     'QuotedUserProfileBackgroundImageUrl', #138
                     'QuotedUserProfileImageUrl', #139
                     'QuotedUserFollowing', #140
                     'QuotedMediaID', #141
                     'QuotedMediaMediaUrl', #142
                     'QuotedMediaUrl', #143
                     'QuotedMediaExpandedUrl', #144
                     'QuotedMediaID', #145
                     'QuotedMediaMediaURL', #146
                     'QuotedInReplyToScreenName'  #147
                     ]
        twitcol = 0
        for header in headerObj:
                twittersheet.write(0,twitcol, header, titles_format)
                twitcol = twitcol + 1
                
        #variables used for progressing through the spreadsheet
        twitrow = 1
        twitcol = 0
        
        #error catching if Twitter box isn't checked/returns 0 results
        if not twitterVariable:
                twittersheet.write(1, 0, "No Twitter Data Found", posts_format)
        else:
                statusList = twitterVariable['statuses']

                #  these are the lists created for entries that require lists.
                #  these include information derived from the dictionary
                #  nested in a list nested in the main dictionary.  In Twitter,
                #  a user might link multiple media links (images, for example)
                #  and in order to capture ALL of these links, they have to put into
                #  a list.  And if there are multiple medias, that means there is
                #  potential for multiple media IDs, Urls, Sources, etc.  This is the
                #  reason for the large number of lists.
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
                retweetedExtendedEntitiesMediaIDStr = []
                retweetedExtendedEntitiesMediaMediaUrl = []
                retweetedExtendedEntitiesMediaUrl = []
                retweetedExtendedEntitiesMediaExpandedUrl = []
                retweetedExtendedEntitiesMediaSourceStatusIDStr = []
                retweetedExtendedEntitiesMediaSourceUserIDStr = []

                #----------NOTE-----------
                #  each of these if-statements below are necessary for error catching.  In some cases,
                #  the if statement is needed because of the way the json file is created.
                #  Sometimes there are dictionaries of lists, while sometimes there are additional
                #  lists of dictionaries nested in these parent dictionaries.  Sometimes loops
                #  are needed to iterate through the available dictionary key.  In each case,
                #  it might be different in the approach to extract the information for the
                #  excel field, but the technique in the if-statements and for-loops are
                #  consistent throughout this document.
                #-------------------------
                
                for entry in statusList:
                        twittersheet.write(twitrow, twitcol, entry['created_at'], posts_format) #1
                        twittersheet.write_url(twitrow, twitcol+1, 'https://www.twitter.com/statuses/'+str(entry['id']), url_format)#2
                        twittersheet.write(twitrow, twitcol+2, entry['text'], posts_format)#3
                        twittersheet.write(twitrow, twitcol+3, '', posts_format)#4 - Blank on purpose - for sentiment analysis
                        twittersheet.write(twitrow, twitcol+4, '', posts_format)#5 - Blank on purpose - for sentiment analysis
                        twittersheet.write(twitrow, twitcol+5, '', posts_format)#6 EMPTYEMPTYEMPTY geo
                        twittersheet.write(twitrow, twitcol+6, '', posts_format)#7 EMPTYEMPTYEMPTY coords
                        twittersheet.write(twitrow, twitcol+7, '', posts_format)#8 EMPTYEMPTYEMPTY contributros
        
                        twittersheet.write(twitrow, twitcol+8, entry['retweet_count'], posts_format)#9
                        twittersheet.write(twitrow, twitcol+9, entry['favorite_count'], posts_format)#10
                        twittersheet.write(twitrow, twitcol+10, str(entry['favorited']), posts_format)#11
                        twittersheet.write(twitrow, twitcol+11, str(entry['retweeted']), posts_format)#12
                        twittersheet.write(twitrow, twitcol+12, '', posts_format)#13 EMPTYEMPTYEMPTY possibly sensitive
                        twittersheet.write(twitrow, twitcol+13, entry['lang'], posts_format)#14
                        twittersheet.write(twitrow, twitcol+14, bool(entry['is_quote_status']), posts_format)#15
                        twittersheet.write(twitrow, twitcol+15, '', posts_format)#16EMPTYEMPTYEMPTY status id str
                        twittersheet.write(twitrow, twitcol+16, '', posts_format)#17EMPTYEMPTYEMPTY user id str
                        twittersheet.write(twitrow, twitcol+17, '', posts_format)#18EMPTYEMPTYEMPTY screen name


                        #'user' block start-------------------
                        if 'user' in entry:
                                twittersheet.write(twitrow, twitcol+18, '', posts_format)#19EMPTYEMPTYEMPTY user id str
                                twittersheet.write_url(twitrow, twitcol+19, 'https://www.twitter.com/'+str(entry['user']['screen_name']), url_format)#20
                                twittersheet.write(twitrow, twitcol+20, entry['user']['location'], posts_format)#21
                                twittersheet.write(twitrow, twitcol+21, entry['user']['description'], posts_format)#22
                                twittersheet.write_url(twitrow, twitcol+22, str(entry['user']['url']), url_format)#23
                                #coming back to these two later url urls url, url urls expanded url
                                #twittersheet.write(twitrow, twitcol+23, entry['user']['location'], posts_format)#24EMPTYEMPTYEMPTY
                                #twittersheet.write(twitrow, twitcol+24, entry['user']['location'], posts_format)#25EMPTYEMPTYEMPTY
                                twittersheet.write(twitrow, twitcol+25, entry['user']['protected'], posts_format)#26
                                twittersheet.write(twitrow, twitcol+26, entry['user']['followers_count'], posts_format)#27
                                twittersheet.write(twitrow, twitcol+27, entry['user']['friends_count'], posts_format)#28
                                twittersheet.write(twitrow, twitcol+28, entry['user']['listed_count'], posts_format)#29
                                twittersheet.write(twitrow, twitcol+29, entry['user']['created_at'], posts_format)#30
                                twittersheet.write(twitrow, twitcol+30, entry['user']['favourites_count'], posts_format)#31
                                twittersheet.write(twitrow, twitcol+31, entry['user']['time_zone'], posts_format)#32
                                twittersheet.write(twitrow, twitcol+32, entry['user']['verified'], posts_format)#33
                                twittersheet.write(twitrow, twitcol+33, entry['user']['lang'], posts_format)#34
                                twittersheet.write(twitrow, twitcol+34, entry['user']['contributors_enabled'], posts_format)#35
                                twittersheet.write_url(twitrow, twitcol+35, str(entry['user']['profile_background_image_url']), url_format)#36
                                twittersheet.write_url(twitrow, twitcol+36, entry['user']['profile_image_url'], url_format)#37
                                twittersheet.write_url(twitrow, twitcol+37, entry['user']['profile_image_url_https'], url_format)#38
                                if 'profile_banner_url' in entry['user']:#39
                                        twittersheet.write_url(twitrow, twitcol+38, entry['user']['profile_banner_url'], url_format)
                                else:
                                        twittersheet.write(twitrow, twitcol+38, 'No banner URL', posts_format)
                                twittersheet.write(twitrow, twitcol+39, entry['user']['following'], posts_format)#40
                                twittersheet.write(twitrow, twitcol+40, '', posts_format)#41 emptyEMPTYEMPTYEMPTY
                        
                        #'user' block end-------------------
                                
                        for mention in entry['entities']['user_mentions']:#42
                                mentionList.append('https://www.twitter.com/'+mention['screen_name']+'\n')
                        twittersheet.write_url(twitrow, twitcol+41, ''.join(mentionList), url_format)
                        twittersheet.write(twitrow, twitcol+42, '', posts_format)#43 EMPTYEMPTYEMPTY
                        twittersheet.write(twitrow, twitcol+43, '', posts_format)#44 EMPTYEMPTYEMPTY
                        twittersheet.write(twitrow, twitcol+44, '', posts_format)#45 EMPTYEMPTYEMPTY
                        if 'entities' in entry:#46
                                if 'media' in entry['entities']:
                                        for item in entry['entities']['media']:
                                               mediaList.append(item['media_url']+'\n')
                        twittersheet.write_url(twitrow, twitcol+45, ''.join(mediaList), url_format)
                        twittersheet.write(twitrow, twitcol+46, '', posts_format)#47 EMPTYEMPTYEMPTY
                        twittersheet.write(twitrow, twitcol+47, '', posts_format)#48 EMPTYEMPTYEMPTY
                        twittersheet.write(twitrow, twitcol+48, '', posts_format)#49 EMPTYEMPTYEMPTY
                        twittersheet.write(twitrow, twitcol+49, '', posts_format)#50 EMPTYEMPTYEMPTY
                        twittersheet.write(twitrow, twitcol+50, '', posts_format)#51 EMPTYEMPTYEMPTY

                        #START - retweeted status----------------------
                        if 'retweeted_status' in entry:
                                twittersheet.write(twitrow, twitcol+51, entry['retweeted_status']['created_at'], posts_format) #52
                                twittersheet.write(twitrow, twitcol+52, entry['retweeted_status']['id_str'], posts_format) #53
                                twittersheet.write(twitrow, twitcol+53, entry['retweeted_status']['text'], posts_format) #54
                                twittersheet.write(twitrow, twitcol+54, '', posts_format)#55 - Blank on purpose - for sentiment analysis
                                twittersheet.write(twitrow, twitcol+55, '', posts_format)#56 - Blank on purpose - for sentiment analysis
                                for item in entry['retweeted_status']['entities']['urls']:
                                        retweetedStatusEntitiesUrlsUrl.append(item['url']+'\n')#57
                                        retweetedStatusEntitiesUrlsExpandedUrl.append(item['expanded_url']+'\n')#58
                                twittersheet.write_url(twitrow, twitcol+56, ''.join(retweetedStatusEntitiesUrlsUrl), url_format)
                                twittersheet.write_url(twitrow, twitcol+57, ''.join(retweetedStatusEntitiesUrlsExpandedUrl), url_format)
                                if 'entities' in entry['retweeted_status']:#59
                                        if 'hashtags' in entry['retweeted_status']['entities']:
                                                for item in entry['retweeted_status']['entities']['hashtags']:
                                                        retweetedEntitiesHashtags.append('#'+item['text']+'\n')
                                twittersheet.write(twitrow, twitcol+58, ''.join(retweetedEntitiesHashtags), posts_format)
                                if 'entities' in entry['retweeted_status']:
                                        if 'user_mentions' in entry['retweeted_status']['entities']:
                                                for item in entry['retweeted_status']['entities']['user_mentions']:
                                                        retweetedUserMentionsScreenNames.append('@'+item['screen_name']+'\n')#60
                                                        retweetedUserMentionsNames.append('@'+item['name']+'\n')#61
                                                        retweetedUserMentionsIDstrs.append('@'+item['id_str']+'\n')#62
                                twittersheet.write(twitrow, twitcol+59, ''.join(retweetedUserMentionsScreenNames), posts_format)
                                twittersheet.write(twitrow, twitcol+60, ''.join(retweetedUserMentionsNames), posts_format)
                                twittersheet.write(twitrow, twitcol+61, ''.join(retweetedUserMentionsIDstrs), posts_format)
                                if 'entities' in entry['retweeted_status']:
                                        if 'media' in entry['retweeted_status']['entities']:
                                                for item in entry['retweeted_status']['entities']['media']:
                                                        retweetedEntitiesMediaIDstr.append(item['id_str']+'\n') #63
                                                        retweetedEntitiesMediaMediaUrl.append(item['media_url']+'\n')#64
                                                        retweetedEntitiesMediaUrl.append(item['url']+'\n')#65
                                                        retweetedEntitiesMediaExpUrl.append(item['expanded_url']+'\n')#66
                                                        if 'source_status_id_str' in item:#67
                                                                retweetedEntitiesMediaSourceStatusID.append(item['source_status_id_str']+'\n')
                                                        if 'source_user_id_str' in item:#68
                                                                retweetedEntitiesMediaSourceUserIDstr.append(item['source_user_id_str']+'\n')
                                twittersheet.write(twitrow, twitcol+62, ''.join(retweetedEntitiesMediaIDstr), posts_format)
                                twittersheet.write_url(twitrow, twitcol+63, ''.join(retweetedEntitiesMediaMediaUrl), url_format)
                                twittersheet.write_url(twitrow, twitcol+64, ''.join(retweetedEntitiesMediaUrl), url_format)
                                twittersheet.write_url(twitrow, twitcol+65, ''.join(retweetedEntitiesMediaExpUrl), url_format)
                                twittersheet.write(twitrow, twitcol+66, ''.join(retweetedEntitiesMediaSourceStatusID), posts_format)
                                twittersheet.write(twitrow, twitcol+67, ''.join(retweetedEntitiesMediaSourceUserIDstr), posts_format)
                                if 'extended_entities' in entry['retweeted_status']:
                                        for item in entry['retweeted_status']['extended_entities']['media']:
                                                retweetedExtendedEntitiesMediaIDStr.append(item['id_str']+'\n')#69
                                                retweetedExtendedEntitiesMediaMediaUrl.append(item['media_url']+'\n')#70
                                                retweetedExtendedEntitiesMediaUrl.append(item['url']+'\n')#71
                                                retweetedExtendedEntitiesMediaExpandedUrl.append(item['expanded_url']+'\n')#72
                                                if 'source_status_id_str' in item:#73
                                                        retweetedExtendedEntitiesMediaSourceStatusIDStr.append(item['source_status_id_str']+'\n')
                                                if 'source_user_id_str' in item:#74
                                                        retweetedExtendedEntitiesMediaSourceUserIDStr.append(item['source_user_id_str']+'\n')
                                twittersheet.write(twitrow, twitcol+68, ''.join(retweetedExtendedEntitiesMediaIDStr), posts_format)
                                twittersheet.write_url(twitrow, twitcol+69, ''.join(retweetedExtendedEntitiesMediaMediaUrl), url_format)
                                twittersheet.write_url(twitrow, twitcol+70, ''.join(retweetedExtendedEntitiesMediaUrl), url_format)
                                twittersheet.write_url(twitrow, twitcol+71, ''.join(retweetedExtendedEntitiesMediaExpandedUrl), url_format)
                                twittersheet.write(twitrow, twitcol+72, ''.join(retweetedExtendedEntitiesMediaSourceStatusIDStr), posts_format)
                                twittersheet.write(twitrow, twitcol+73, ''.join(retweetedExtendedEntitiesMediaSourceUserIDStr), posts_format)
                                if 'metadata' in entry['retweeted_status']:#75
                                        twittersheet.write(twitrow, twitcol+74, entry['retweeted_status']['metadata']['iso_language_code'], posts_format)
                                twittersheet.write(twitrow, twitcol+75, entry['retweeted_status']['source'], posts_format)#76
                                twittersheet.write(twitrow, twitcol+76, entry['retweeted_status']['in_reply_to_status_id_str'], posts_format)#77
                                twittersheet.write(twitrow, twitcol+77, entry['retweeted_status']['in_reply_to_user_id_str'], posts_format)#78
                                twittersheet.write(twitrow, twitcol+78, entry['retweeted_status']['in_reply_to_screen_name'], posts_format)#79
                                twittersheet.write(twitrow, twitcol+79, entry['retweeted_status']['user']['name'], posts_format)#80
                                twittersheet.write(twitrow, twitcol+80, entry['retweeted_status']['user']['screen_name'], posts_format)#81
                                twittersheet.write(twitrow, twitcol+81, entry['retweeted_status']['user']['location'], posts_format)#82
                                twittersheet.write(twitrow, twitcol+82, entry['retweeted_status']['user']['description'], posts_format)#83
                                twittersheet.write_url(twitrow, twitcol+83, str(entry['retweeted_status']['user']['url']), url_format)#84
                                twittersheet.write(twitrow, twitcol+84, '', posts_format)#85 EMPTYEMPTYEMPTY
                                twittersheet.write(twitrow, twitcol+85, '', posts_format)#86 EMPTYEMPTYEMPTY
                                twittersheet.write(twitrow, twitcol+86, entry['retweeted_status']['user']['followers_count'], posts_format)#87
                                twittersheet.write(twitrow, twitcol+87, entry['retweeted_status']['user']['friends_count'], posts_format)#88
                                twittersheet.write(twitrow, twitcol+88, entry['retweeted_status']['user']['listed_count'], posts_format)#89
                                twittersheet.write(twitrow, twitcol+89, entry['retweeted_status']['user']['created_at'], posts_format)#90
                                twittersheet.write(twitrow, twitcol+90, entry['retweeted_status']['user']['favourites_count'], posts_format)#91
                                twittersheet.write(twitrow, twitcol+91, entry['retweeted_status']['user']['time_zone'], posts_format)#92
                                twittersheet.write(twitrow, twitcol+92, entry['retweeted_status']['user']['verified'], posts_format)#93
                                twittersheet.write(twitrow, twitcol+93, entry['retweeted_status']['user']['lang'], posts_format)#94
                                twittersheet.write_url(twitrow, twitcol+94, str(entry['retweeted_status']['user']['profile_background_image_url']), url_format)#95
                                twittersheet.write_url(twitrow, twitcol+95, str(entry['retweeted_status']['user']['profile_image_url']), url_format)#96
                                twittersheet.write(twitrow, twitcol+96, entry['retweeted_status']['user']['following'], posts_format)#97
                                twittersheet.write(twitrow, twitcol+97, entry['retweeted_status']['geo'], posts_format)#98
                                #coordinates is messing up, commenting out for now #99
                                #twittersheet.write(twitrow, twitcol+98, entry['retweeted_status']['coordinates'], posts_format)
                                #place requires this if/else statement and error catcher like it did before
                                if entry['retweeted_status']['place'] != None:#100
                                        if 'country' in entry['retweeted_status']['place']:
                                                twittersheet.write(twitrow, twitcol+99, entry['retweeted_status']['place']['country'], posts_format)
                                        else:
                                                twittersheet.write(twitrow, twitcol+99, 'No country listed', posts_format)
                                twittersheet.write(twitrow, twitcol+100, entry['retweeted_status']['is_quote_status'], posts_format)#101
                                twittersheet.write(twitrow, twitcol+101, entry['retweeted_status']['retweet_count'], posts_format)#102
                                twittersheet.write(twitrow, twitcol+102, entry['retweeted_status']['favorite_count'], posts_format)#103
                                twittersheet.write(twitrow, twitcol+103, entry['retweeted_status']['favorited'], posts_format)#104
                                twittersheet.write(twitrow, twitcol+104, entry['retweeted_status']['retweeted'], posts_format)#105
                                if 'possibly_sensitive' in ['retweeted_status']:#106
                                        twittersheet.write(twitrow, twitcol+105, entry['retweeted_status']['possibly_sensitive'], posts_format)
                                else:
                                        twittersheet.write(twitrow, twitcol+105, 'DNE', posts_format)
                                twittersheet.write(twitrow, twitcol+106, entry['retweeted_status']['lang'], posts_format) #107
                                if 'quoted_status' in entry['retweeted_status']:
                                        twittersheet.write(twitrow, twitcol+107, entry['retweeted_status']['quoted_status']['created_at'], posts_format)#108
                                        twittersheet.write(twitrow, twitcol+108, entry['retweeted_status']['quoted_status']['id_str'], posts_format)#109
                                        twittersheet.write(twitrow, twitcol+109, entry['retweeted_status']['quoted_status']['text'], posts_format)#110 if 'entities' in entry['quoted_status']:
                                twittersheet.write(twitrow, twitcol+110, '', posts_format)#111 - Blank on purpose - for sentiment analysis
                                twittersheet.write(twitrow, twitcol+111, '', posts_format)#112 - Blank on purpose - for sentiment analysis
                                if 'quoted_status' in entry['retweeted_status']:
                                        if 'media' in entry['retweeted_status']['quoted_status']['entities']:
                                                for item in entry['retweeted_status']['quoted_status']['entities']['media']:
                                                        entitiesMediaIDstr.append(item['id_str']+'\n')#113
                                                        entitiesMediaMediaUrlList.append(item['media_url']+'\n')#114
                                                        entitiesMediaUrlList.append(item['url']+'\n')#115
                                                        entitiesMediaExpandedUrlList.append(item['expanded_url']+'\n')#116
                                twittersheet.write(twitrow, twitcol+112, ''.join(entitiesMediaIDstr), posts_format)
                                twittersheet.write_url(twitrow, twitcol+113, ''.join(entitiesMediaMediaUrlList), url_format)
                                twittersheet.write_url(twitrow, twitcol+114, ''.join(entitiesMediaUrlList), url_format)
                                twittersheet.write_url(twitrow, twitcol+115, ''.join(entitiesMediaExpandedUrlList), url_format)
                        
                        #END - retweeted status----------------------

                        #START - quoted_status-------------------

                        if 'quoted_status' in entry:
                                #for Testing: to make sure you get hits for search results that have a quoted status, search for
                                #'statuses' for twitter
                                if 'extended_entities' in entry['quoted_status']:
                                        for item in entry['quoted_status']['extended_entities']['media']:
                                                quotedMediaIDList.append(item['id_str']+'\n')#117
                                                quotedMediaList.append(item['media_url']+'\n')#118
                                        twittersheet.write_url(twitrow, twitcol+116, ''.join(quotedMediaIDList), url_format)
                                        twittersheet.write_url(twitrow, twitcol+117, ''.join(quotedMediaList), url_format)
                                else: 
                                        twittersheet.write(twitrow, twitcol+116, 'No media url ID', posts_format)                                
                                        twittersheet.write(twitrow, twitcol+117, 'No media url', posts_format)
                                twittersheet.write(twitrow, twitcol+118, entry['quoted_status']['in_reply_to_screen_name'], posts_format)#119
                                twittersheet.write(twitrow, twitcol+119, entry['quoted_status']['user']['name'], posts_format)#120
                                twittersheet.write(twitrow, twitcol+120, entry['quoted_status']['user']['screen_name'], posts_format)#121
                                twittersheet.write(twitrow, twitcol+121, entry['quoted_status']['user']['location'], posts_format)#122
                                twittersheet.write(twitrow, twitcol+122, entry['quoted_status']['user']['description'], posts_format)#123
                                twittersheet.write_url(twitrow, twitcol+123, str(entry['quoted_status']['user']['url']), url_format)#124
                                twittersheet.write(twitrow, twitcol+124, '', posts_format)#125 EMPTYEMPTYEMPTY
                                twittersheet.write(twitrow, twitcol+125, '', posts_format)#126 EMPTYEMPTYEMPTY
                                
                                #if error is list indices must be integers not strings, it means that within the dictionary,
                                #there is a list you must access.  Haven't found the best way to do this
                                #UPDATE: as a workaround, the way to fix this is to treat it as a list. See below how 'id_str' was
                                #fixed - it was giving me the same errors before.
                                
                                twittersheet.write(twitrow, twitcol+126, entry['quoted_status']['user']['followers_count'], posts_format)#127
                                twittersheet.write(twitrow, twitcol+127, entry['quoted_status']['user']['friends_count'], posts_format)#128
                                twittersheet.write(twitrow, twitcol+128, entry['quoted_status']['user']['listed_count'], posts_format)#129
                                twittersheet.write(twitrow, twitcol+129, entry['quoted_status']['user']['created_at'], posts_format)#130
                                twittersheet.write(twitrow, twitcol+130, entry['quoted_status']['user']['favourites_count'], posts_format)#131
                                twittersheet.write(twitrow, twitcol+131, entry['quoted_status']['user']['time_zone'], posts_format)#132
                                twittersheet.write(twitrow, twitcol+132, entry['quoted_status']['user']['lang'], posts_format)#133
                                #background image required this error catching to function
                                if entry['quoted_status']['user']['profile_background_image_url'] != None: #134
                                        twittersheet.write_url(twitrow, twitcol+133, entry['quoted_status']['user']['profile_background_image_url'], url_format)
                                else:
                                        twittersheet.write(twitrow, twitcol+133, 'No background image url', posts_format)
                                twittersheet.write_url(twitrow, twitcol+134, entry['quoted_status']['user']['profile_image_url'], url_format)#135
                                twittersheet.write(twitrow, twitcol+135, bool(entry['quoted_status']['user']['following']), posts_format)#136
                                twittersheet.write(twitrow, twitcol+136, entry['quoted_status']['geo'], posts_format)#137
                                
                                #this one row below with coordinates was throwing an error of 'Unsupported type <type 'dict'> in write()'
                                #commenting it out for now
                                twittersheet.write(twitrow, twitcol+137, '', posts_format) #138 EMPTYEMPTYEMPTY
                                #twittersheet.write(twitrow, twitcol+20, entry['quoted_status']['coordinates'], posts_format)
                                #['quoted_status']['place'] was throwing errors if I didn't use this double if-statement
                                
                                if entry['quoted_status']['place'] != None: #139
                                        if 'country' in entry['quoted_status']['place']:
                                                twittersheet.write(twitrow, twitcol+138, entry['quoted_status']['place']['country'], posts_format)
                                        else:
                                                twittersheet.write(twitrow, twitcol+138, 'No country listed', posts_format)
                                twittersheet.write(twitrow, twitcol+139, str(entry['quoted_status']['is_quote_status']), posts_format)#140
                                twittersheet.write(twitrow, twitcol+140, entry['quoted_status']['retweet_count'], posts_format)#141
                                twittersheet.write(twitrow, twitcol+141, entry['quoted_status']['favorite_count'], posts_format)#142
                                twittersheet.write(twitrow, twitcol+142, str(entry['quoted_status']['favorited']), posts_format)#143
                                twittersheet.write(twitrow, twitcol+143, str(entry['quoted_status']['retweeted']), posts_format)#144
                                twittersheet.write(twitrow, twitcol+144, '', posts_format)#145 EMPTYEMPTYEMPTY
                                twittersheet.write(twitrow, twitcol+145, entry['quoted_status']['lang'], posts_format)#146
                                
                        

                        #END - quoted_status-------------------
        
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
	
