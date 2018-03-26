import sys, os

import praw

import redditAPI, twitterAPI

def searchHandle(query, apiSelectArray):

	redditResults = ""
	twitterResults = ""

	print(apiSelectArray)

	if 'reddit' in apiSelectArray:

		print("Inside Reddit If.")

		redditResults = redditAPI.search(query)

	if 'twitter' in apiSelectArray:

		print('Inside Twitter If.')

		twitterResults = twitterAPI.search(query)

	#print(redditResults, twitterResults)
	return redditResults, twitterResults