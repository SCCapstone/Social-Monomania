import sys, os

import praw

import redditAPI, twitterAPI

def searchHandle(query, apiSelectArray, reddit_Subreddits, twitterDate):

	redditResults = ""
	twitterResults = ""

	print(apiSelectArray)

	if 'reddit' in apiSelectArray:

		redditResults = redditAPI.search(query, reddit_Subreddits)

	if 'twitter' in apiSelectArray:

		twitterResults = twitterAPI.search(query, twitterDate)

	# print(twitterResults)
	# print(redditResults)
	return redditResults, twitterResults