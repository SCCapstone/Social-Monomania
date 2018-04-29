import sys, os

import urllib
import urllib2
import json, csv

import oauth2


CONSUMER_KEY = "VFDbTduxt6SeTwyOjOFIfwWIO"
CONSUMER_SECRET = "MrfTScFm6APqTZxDC5cwVAfSVqy5UCbgj61nl6Q34psjcs7J5F"

def search(args, date = '', geocode = None):

	query = urllib.quote_plus(args)

	if (date == '' and geocode == None):
		url = "https://api.twitter.com/1.1/search/tweets.json?q={0}&count=100".format(query)

	elif (geocode == None):
		url = "https://api.twitter.com/1.1/search/tweets.json?q={0}&until={1}&count=100".format(query,date)

	#r = urllib2.urlopen(url)
	#resultJSON = r.readline().decode('utf-8')
	resultJSON = oauth_req(url, '3270317358-uXCQfUGY86T1EBPIrGX97s7EkNzzZide84mfgHo' , 'CCdhkak0eOQDxfdAcbdfCkHn91Hdd5SMlldbLtOQFpfPw')
	result_parsed = json.loads(resultJSON)
	next_results = result_parsed.get('search_metadata').get('next_results')
	if (next_results != None):
		next_url= "https://api.twitter.com/1.1/search/tweets.json"+next_results

	for i in range(1,10):
		resultJSONLoop = oauth_req(next_url, '3270317358-uXCQfUGY86T1EBPIrGX97s7EkNzzZide84mfgHo' , 'CCdhkak0eOQDxfdAcbdfCkHn91Hdd5SMlldbLtOQFpfPw')
		result_parsedLoop = json.loads(resultJSONLoop)
		

		for status in result_parsedLoop.get('statuses'):
			result_parsed.get('statuses').append(status)

		next_results = result_parsedLoop.get('search_metadata').get('next_results')
		if (next_results != None):
			next_url= "https://api.twitter.com/1.1/search/tweets.json"+next_results

	return result_parsed


def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):

    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret= CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content

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