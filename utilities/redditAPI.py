import sys, os

import json
import time, datetime

import praw

def search(args = None):

	if(args == None):
		args = sys.argv[1:]

	reddit = praw.Reddit(client_id='dL9KuOJHJojZaw',
                     client_secret='ek3X-TenXuiWDRzbXfSPROUglvg',
                     user_agent='Social Monomania API Searcher (by /u/Sorrento110')

	relevant_submissions = []
	retInfo = {}

	# params = {'sort':'new', 'limit':None, 'syntax':'cloudsearch'}
	# time_now = datetime.datetime.now()

	for submission in reddit.subreddit('news').new(limit=None):
		##Not decided on which reddit calls will give us the best results. Still experimenting.
		if (args.lower() in submission.title.lower()):
			relevant_submissions.append(submission)

	print(relevant_submissions)
	##Testing submission accesses; this submission will be stored in specific variables and passed to the handler,
	## which will then access these specifics

	for submission in relevant_submissions:

		timep = submission.created
		timestamp = datetime.date.fromtimestamp(timep)

		retInfo[submission.title] = {
			'time' : timestamp,
			'url'  : "http://www.reddit.com" + submission.permalink
		}

	#print("DID REDDIT!")
	print(retInfo)
	return retInfo

if __name__ == '__main__':

	args = sys.argv[1:]

	search(args[0])





#reddit.subreddit('news').search('timestamp:{0}..{1}'.format(int(time.mktime(time_now.timetuple()) - datetime.timedelta(days=365).total_seconds()), int(time.mktime(time_now.timetuple()))), params)