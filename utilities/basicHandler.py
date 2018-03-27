import sys, os

import praw

import redditAPI, twitterAPI

def searchHandle(query, apiSelectArray):

	redditResults = ""
	twitterResults = ""

	print(apiSelectArray)

	if 'reddit' in apiSelectArray:

		redditResults = redditAPI.search(query)

	if 'twitter' in apiSelectArray:

		twitterResults = twitterAPI.search(query)

	#print(twitterResults)
	return redditResults, twitterResults