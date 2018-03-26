import sys, os

import urllib
import urllib2
import json, csv
import oauth2
import unicodedata


CONSUMER_KEY = "VFDbTduxt6SeTwyOjOFIfwWIO"
CONSUMER_SECRET = "MrfTScFm6APqTZxDC5cwVAfSVqy5UCbgj61nl6Q34psjcs7J5F"

def search(args):

	query = urllib.quote_plus(args)

	url = "https://api.twitter.com/1.1/search/tweets.json?q={0}".format(query)

	#r = urllib2.urlopen(url)
	#resultJSON = r.readline().decode('utf-8')
	resultJSON = oauth_req(url, '3270317358-uXCQfUGY86T1EBPIrGX97s7EkNzzZide84mfgHo' , 'CCdhkak0eOQDxfdAcbdfCkHn91Hdd5SMlldbLtOQFpfPw')
	result_parsed = json.loads(resultJSON)
	statuses = result_parsed.get("statuses")
	# f = open('twitter.txt', 'w')
	# # for x in statuses:
	# # 	print x.get("user").get("screen_name")
	# # 	f.write(x.get("user").get("screen_name").encode("UTF-8") +": " + x.get("text").encode("UTF-8") +"\n")
	# f.close()
	#print("DID TWITTER!")
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