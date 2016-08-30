from django.test import Client, TestCase
from base.models import Project


class TestProject(TestCase):
	def testProjectShouldBeCreateOverForm(self):
		# When
		Project.objects.all().delete()
		response = Client().post('/ui/createproject', data={'name': 'test_project'})
		# Then
		self.assertEqual(response.status_code, 200)
		Project.objects.get(name='test_project')		# Not raise
