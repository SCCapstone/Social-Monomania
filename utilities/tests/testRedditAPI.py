from django.test import TestCase

from ..redditAPI import search

class RedditTestCase(TestCase):
	"""Unit test to ensure that search string is found in 100 new reddit posts returned from API"""
	def setUp(self):
		self.queryString = "SC"
		self.submissions = search(self.queryString)


	def test_submissions_contain_query(self):
		for submission in self.submissions:
			self.assertTrue(self.queryString in submission.title)
