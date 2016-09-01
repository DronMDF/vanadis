from django.test import Client, TestCase
from base.models import Project


class TestMainPage(TestCase):
	def testRootPageRedirectToUI(self):
		# When
		response = Client().get('/')
		# Then
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, '/ui')

	def testProjectListShowOnMainPage(self):
		# Given
		Project.objects.all().delete()
		Project.objects.create(name='test1')
		Project.objects.create(name='test2')
		# When
		response = Client().get('/ui/')
		# Then
		self.assertEqual(response.status_code, 200)
		text = response.content.decode('utf-8')
		self.assertIn('test1', text)
		self.assertIn('test2', text)
