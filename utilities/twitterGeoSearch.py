import sys, os

import urllib
import urllib2
import json, csv

import oauth2

CONSUMER_KEY = "VFDbTduxt6SeTwyOjOFIfwWIO"
CONSUMER_SECRET = "MrfTScFm6APqTZxDC5cwVAfSVqy5UCbgj61nl6Q34psjcs7J5F"

def geoSearch(args):

	query = urllib.quote_plus(args)

	url = "https://api.twitter.com/1.1/geo/search.json?query={0}".format(query)

	resultJSON = oauth_req(url, '3270317358-uXCQfUGY86T1EBPIrGX97s7EkNzzZide84mfgHo' , 'CCdhkak0eOQDxfdAcbdfCkHn91Hdd5SMlldbLtOQFpfPw')
	result_parsed = json.loads(resultJSON)

	geocodeArray = result_parsed.get('result').get('places')
	coordsArray = geocodeArray[0].get('bounding_box').get('coordinates')[0][0]

	print(coordsArray)
	return coordsArray



#Default Twitter function to generate an info object
def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):

    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret= CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    #Call to Twitter happens here.
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content