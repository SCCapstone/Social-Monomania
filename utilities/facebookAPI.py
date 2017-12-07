import sys, os

import urllib2
import json


def search(args = None):

	if(args == None):
		args = sys.argv[1:]

	query = args
	access_token = "EAACMUxD9QFwBAP3JReCVOxRsSNZAczKtfbvPlFw3UkZARAzeFbbZAF6Bg19jaSHEVLDg6QFmQwZCh2x3KNsPOPgTLnZBbsZC1vQHCblTaBuhJ7WiMhEttCbqd3V65THGb3dXP97KgkK0dWmrssSj0IbXzCZAtxBIpX5K0kQlcZAuHxfWO9e7aNjg3sTDK4AXskE8YiR3OBwFxwZDZD"

	url = "https://graph.facebook.com/search?access_token={0}&q={1}&type=event".format(access_token, query)
	print(url)

	r = urllib2.urlopen(url)
	resultJSON = r.readline().decode('utf-8')
	result = json.loads(resultJSON)

	result['data'] = [ item for item in result['data']
                   if query.lower() in item['name'].lower() ]

	print [ item['name'] for item in result['data'] ]

if __name__ == '__main__':

	args = sys.argv[1:]

	search(args[0])

