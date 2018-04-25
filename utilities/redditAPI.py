import sys, os

import json
import datetime

import praw

def search(args = None, subreddits = ['news']):

	if(args == None):
		args = sys.argv[1:]

	reddit = praw.Reddit(client_id='dL9KuOJHJojZaw',
                     client_secret='ek3X-TenXuiWDRzbXfSPROUglvg',
                     user_agent='Social Monomania API Searcher (by /u/Sorrento110')

	all_submissions = []
	relevant_submissions = []
	retInfo = {}
	
	print(subreddits)
	query_these_subreddits = subredditStringGenerator(subreddits)

	Redditbatch = reddit.subreddit(query_these_subreddits).search(args, sort='new', time_filter='all')

	for submission in Redditbatch:
		##Not decided on which reddit calls will give us the best results. Still experimenting.
		if (args.lower() in submission.title.lower()):
			relevant_submissions.append(submission)

	#print(relevant_submissions)
	##Testing submission accesses; this submission will be stored in specific variables and passed to the handler,
	## which will then access these specifics

	for submission in relevant_submissions:

		time = submission.created_utc
		timestamp = datetime.date.fromtimestamp(time)

		retInfo[submission.title] = {
			'time'       : timestamp,
			'url'        : "http://www.reddit.com" + submission.permalink,
			'upvotes'    : submission.score,
			'source_sub' : submission.subreddit,
			'comments'   : submission.num_comments
			}

	#print("DID REDDIT!")
	#print(retInfo)
	return retInfo

def subredditStringGenerator(subreddits):

	subreddit_string =""

	#Getting the proper subreddit string
	for string in subreddits:
		subreddit_string += string
		subreddit_string += '+'

	subreddit_string = subreddit_string[:-1]

	return subreddit_string


if __name__ == '__main__':

	args = sys.argv[1:]

	search(args[0])














#reddit.subreddit('news').search('timestamp:{0}..{1}'.format(int(time.mktime(time_now.timetuple()) - datetime.timedelta(days=365).total_seconds()), int(time.mktime(time_now.timetuple()))), params)