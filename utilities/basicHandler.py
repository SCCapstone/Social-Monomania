import sys, os

import praw

import redditAPI, twitterAPI

def searchHandle(query, apiSelectArray):

	redditResults = ""
	twitterResults = ""

	print(apiSelectArray)

	#Logic chunk to call API's based on selected social media site.
	if 'reddit' in apiSelectArray:

		redditResults = redditAPI.search(query)

	if 'twitter' in apiSelectArray:

		twitterResults = twitterAPI.search(query)

	# print(twitterResults)
	# print(redditResults)
	return redditResults, twitterResults