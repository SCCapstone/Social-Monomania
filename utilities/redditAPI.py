import sys, os

import urllib.request
import json

import praw

def search(args = None):

	if(args == None):
		args = sys.argv[1:]

	reddit = praw.Reddit(client_id='dL9KuOJHJojZaw',
                     client_secret='ek3X-TenXuiWDRzbXfSPROUglvg',
                     user_agent='Social Monomania API Searcher (by /u/Sorrento110')

	for submission in reddit.subreddit('news').all(limit=100):
		
