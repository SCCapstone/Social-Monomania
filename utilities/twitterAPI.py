import sys, os

import urllib
import urllib2
import json, csv

import oauth2

import twitterGeoSearch as TGS


CONSUMER_KEY = "VFDbTduxt6SeTwyOjOFIfwWIO"
CONSUMER_SECRET = "MrfTScFm6APqTZxDC5cwVAfSVqy5UCbgj61nl6Q34psjcs7J5F"

def search(args, date = '', geocode = '', radius = "100mi"):

	query = urllib.quote_plus(args)

	coords = []

	#Normal search function uses this chunk. Formats URL without advance search features/if they aren't set.
	if (date == '' and geocode == ''):
		url = "https://api.twitter.com/1.1/search/tweets.json?q={0}&count=100".format(query)

	#Formats URL for just time input plus query (but not geocode).
	elif (geocode == ''):
		url = "https://api.twitter.com/1.1/search/tweets.json?q={0}&until={1}&count=100".format(query,date)

	#Formats URL for Lat/Lon from geocode API call and formats URL for geocode filtering (but not date).
	elif (date == ''):
		coords = TGS.geoSearch(geocode)
		if(radius == ""):
			radius = "100mi"
		geostring = "{0},{1},{2}".format(coords[1],coords[0],radius)

		url = "https://api.twitter.com/1.1/search/tweets.json?q={0}&geocode={1}&count=100".format(query,geostring)

		print url

	#Formats URL for location filtering and date filtering.
	else:
		coords = TGS.geoSearch(geocode)
		if(radius == ""):
			radius = "10mi"
		geostring = "{0},{1},{2}".format(coords[1],coords[0],radius)

		url = "https://api.twitter.com/1.1/search/tweets.json?q={0}&until={1}&geocode={2}&count=100".format(query,date,geostring)


	#Gets the results from twitter in this chunk and parses them from JSON.
	resultJSON = oauth_req(url, '3270317358-uXCQfUGY86T1EBPIrGX97s7EkNzzZide84mfgHo' , 'CCdhkak0eOQDxfdAcbdfCkHn91Hdd5SMlldbLtOQFpfPw')
	result_parsed = json.loads(resultJSON)

	#Gets the next result url from Twitter.
	next_results = None
	try:
		next_results = result_parsed.get('search_metadata').get('next_results')
	except Exception as e:
		print(e)

	next_url = ""
	if (next_results != None):
		next_url= "https://api.twitter.com/1.1/search/tweets.json"+next_results

	#Loop to continue calling Twitter over and over to get more results. Appends to initial results object.
	for i in range(1,10):
		if(next_url != ""):
			resultJSONLoop = oauth_req(next_url, '3270317358-uXCQfUGY86T1EBPIrGX97s7EkNzzZide84mfgHo' , 'CCdhkak0eOQDxfdAcbdfCkHn91Hdd5SMlldbLtOQFpfPw')
		else:
			break
		result_parsedLoop = json.loads(resultJSONLoop)
		

		for status in result_parsedLoop.get('statuses'):
			result_parsed.get('statuses').append(status)

		next_results = result_parsedLoop.get('search_metadata').get('next_results')
		next_url = ""
		if (next_results != None):
			next_url= "https://api.twitter.com/1.1/search/tweets.json"+next_results

	return result_parsed

#Default Twitter function to generate an info object
def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):

    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret= CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    #Call to Twitter happens here.
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content

#Function to enable running API call from cmd.
if __name__ == '__main__':

	args = sys.argv[1:]
	argString = ""

	if(len(args) > 1):
		for s in args:
			argString += s + " "
		args = argString
	else:
		args = args[0]

	search(args)