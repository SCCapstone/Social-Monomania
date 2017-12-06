import sys, os

import urllib.request
import json

import facebook

def search(args = None):

	if(args == None):
		args = sys.argv[1:]
	try:
		##### Call to get a different kind of access token commented out.  Using a 'User Access Token'
	# url = "https://graph.facebook.com/oauth/access_token?client_id=154288395206748&client_secret=b31c53b79daff5a17ac4849c839ae998&grant_type=client_credentials"
	# response = urllib.request.urlopen(url)
	# tokenJSON = response.readline().decode('utf-8')
	# token = json.loads(tokenJSON)
		graph = facebook.GraphAPI(access_token="EAACMUxD9QFwBAIWJ1Oy6aW7cSOb2t4Udyu7rMhS8pQoZARMulQKawhhdzOKDnrj3pXZC0RkBcnNx2InPTcz4I43sIcUs8vUkhCZCJgkoCTaH8mI2yUJknt3kNr09rZBN3bpYXQfjPb0eGHfTWm5zn03UD4zw5GnicUT8CVdRbv1OOkUsmoX9iZBvkbsk3CHDFApWgvbpacAZDZD", 
		version="2.10")
	except Exception as e:
		print(e)
	else:
		print("Facebook Graph API initialization Success")



	data = graph.search(type='event', q=args[0])
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
			#Once we discover the fields we want to pull on return we can use this loop to append them to a string and display that to the user.
			results += str(d) + ":" + str(k) + " \n"
		i += 1

	return data
