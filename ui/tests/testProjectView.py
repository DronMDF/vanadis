from django.test import Client, TestCase
from base.models import Project


class TestProjectView(TestCase):
	def testProjectSettingView(self):
		# Given
		Project.objects.all().delete()
		p = Project.objects.create(name='setp')
		# When
		reply = Client().get('/ui/project/setp?setting')
		# Then
		self.assertEqual(reply.status_code, 200)
