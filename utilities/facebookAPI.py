import sys, os

import urllib.request
import json

import facebook

def search(args = None):

	if(args == None):
		args = sys.argv[1:]
	try:
	# url = "https://graph.facebook.com/oauth/access_token?client_id=154288395206748&client_secret=b31c53b79daff5a17ac4849c839ae998&grant_type=client_credentials"
	# response = urllib.request.urlopen(url)
	# tokenJSON = response.readline().decode('utf-8')
	# token = json.loads(tokenJSON)
		graph = facebook.GraphAPI(access_token="EAACMUxD9QFwBAPBhuWV7berbZB7PCoI8uqhaqFatOYhWXnZAWYXjsky2nZCJezytZAzT4CU3H0uwIbAQRIXZCgy94RdhqCZBO4p3lfYtUkbZCNrWIrGCM8vw0YSqQZBg7LkLJSZBTnKtf8DZAwYgKQlcUzh1A51JW3m4fkZBwYFNuRKwwmE9rKIR16MtshnHe48S1QZD", 
		version="2.10")
	except Exception as e:
		print(e)
	else:
		print("Facebook Graph API initialization Success")



	data = graph.search(type='event', q=args[0])
	#dataReadable = json.loads(data)
	print(data)

	results = ''
	i = 1
	for d in data:
		results += "Entry " + str(i) + "--\n"
		for k in d:
			try:
				print(str(d) + ":" + str(k))
			except Exception as e:
				print(e)
			results += str(d) + ":" + str(k) + " \n"
		i += 1

	return results
