from django.test import Client, TestCase
from base.models import Project


class TestNewProjectView(TestCase):
	def testT2IsCorrectProjectName(self):
		# When
		response = Client().post('/ui/newproject', data={'name': 't2'})
		# Then
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, '/ui/project/t2')
		Project.objects.get(name='t2')		# Not raise
