import sys, os

import json

import praw

def search(args = None):

	if(args == None):
		args = sys.argv[1:]

	reddit = praw.Reddit(client_id='dL9KuOJHJojZaw',
                     client_secret='ek3X-TenXuiWDRzbXfSPROUglvg',
                     user_agent='Social Monomania API Searcher (by /u/Sorrento110')

	relevant_submissions = []
	for submission in reddit.subreddit('southcarolina').new(limit=100):
		##Not decided on which reddit calls will give us the best results. Still experimenting.
		if (args in submission.title):
			relevant_submissions.append(submission)

	# print(relevant_submissions)
	return relevant_submissions

if __name__ == '__main__':

	args = sys.argv[1:]

	search(args[0])

