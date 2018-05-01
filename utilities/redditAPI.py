import sys, os

import json
import datetime

import praw

def search(args = None, subreddits = ['news']):

	#Allows for testing from cmd.
	if(args == None):
		args = sys.argv[1:]

	#Initializing reddit object through PRAW with client id and secret.  User agent is a suggested field for reddit devs.
	reddit = praw.Reddit(client_id='dL9KuOJHJojZaw',
                     client_secret='ek3X-TenXuiWDRzbXfSPROUglvg',
                     user_agent='Social Monomania API Searcher (by /u/Sorrento110')

	all_submissions = []
	relevant_submissions = []
	retInfo = {}
	
	#print(subreddits)
	#Calls helper function to change subreddits object to the string PRAW needs.
	query_these_subreddits = subredditStringGenerator(subreddits)

	#Main PRAW call to get results.
	Redditbatch = reddit.subreddit(query_these_subreddits).search(args, sort='new', time_filter='all')

	#Gets submissions from batch and transfers to holder object.
	for submission in Redditbatch:
		relevant_submissions.append(submission)

	#Takes info from each submissions and extracts detailed info into final return object.
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


#Function to enable running API call from cmd.
if __name__ == '__main__':

	args = sys.argv[1:]

	search(args[0])

