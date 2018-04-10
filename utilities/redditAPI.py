import sys, os

import json
import datetime

import praw

def search(args = None):

	if(args == None):
		args = sys.argv[1:]

	reddit = praw.Reddit(client_id='dL9KuOJHJojZaw',
                     client_secret='ek3X-TenXuiWDRzbXfSPROUglvg',
                     user_agent='Social Monomania API Searcher (by /u/Sorrento110')

	relevant_submissions = []
	retInfo = {}

	submission_titles = []

	for submission in reddit.subreddit('news').new(limit=500):
		##Not decided on which reddit calls will give us the best results. Still experimenting.
		if (args.lower() in submission.title.lower()):
			relevant_submissions.append(submission)
			submission_titles.append(submission.title)

	print(relevant_submissions)
	##Testing submission accesses; this submission will be stored in specific variables and passed to the handler,
	## which will then access these specifics
	print (submission_titles)

	for submission in relevant_submissions:

		time = submission.created
		timestamp = datetime.date.fromtimestamp(time)

		retInfo[submission.title] = {
			'time' : timestamp,
			'url'  : submission.url
		}

	print("DID REDDIT!")
	print(retInfo)
	return retInfo

if __name__ == '__main__':

	args = sys.argv[1:]

	search(args[0])

