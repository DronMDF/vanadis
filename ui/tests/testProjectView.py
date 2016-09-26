from django.test import Client, TestCase
from base.models import Project


class TestProjectSettingsView(TestCase):
	def testProjectSettingView(self):
		# Given
		Project.objects.all().delete()
		p = Project.objects.create(name='setp')
		# When
		reply = Client().get('/ui/setp/settings')
		# Then
		self.assertEqual(reply.status_code, 200)

	def testProjectSettingsUrl(self):
		# Given
		Project.objects.all().delete()
		p = Project.objects.create(name='setp')
		# When
		reply = Client().get('/ui/project/setp/')
		# Then
		self.assertEqual(reply.status_code, 200)
		self.assertIn("href='/ui/setp/settings'", reply.content.decode('utf-8'))
