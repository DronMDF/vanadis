from django.test import Client, TestCase
from base.models import Project


class TestProjectSettingsView(TestCase):
	def testProjectSettingView(self):
		# Given
		Project.objects.all().delete()
		Project.objects.create(name='setp')
		# When
		reply = Client().get('/setp/settings')
		# Then
		self.assertEqual(reply.status_code, 200)
		self.assertIn("action='/setp/settings'", reply.content.decode('utf8'))

	def testProjectSettingPost(self):
		# Given
		Project.objects.all().delete()
		Project.objects.create(name='setm')
		# When
		reply = Client().post('/setm/settings', data={'repo_url': 'git://none'})
		# Then
		self.assertEqual(reply.status_code, 302)
		self.assertEqual(reply.url, '/setm')
		self.assertEqual(Project.objects.get(name='setm').repo_url, 'git://none')
