from django.test import Client, TestCase
from base.models import Project


class TestRevisionView(TestCase):
	def testPageShowPreviousUrl(self):
		# Given
		Project.objects.create(name='project', repo_url='file:///tmp/test')
		# When
		response = Client().get('/project/67c47e6')
		# Then
		self.assertEqual(response.status_code, 200)
		self.assertIn("href='/project/1f8b852'", response.content.decode('utf-8'))

	def testNotHeadRevisionShowPreviousUrl(self):
		# Given
		Project.objects.create(name='project', repo_url='file:///tmp/test')
		# When
		response = Client().get('/project/1f8b852')
		# Then
		self.assertEqual(response.status_code, 200)
		self.assertIn("href='/project/e47cdf1'", response.content.decode('utf-8'))
