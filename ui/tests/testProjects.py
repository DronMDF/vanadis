from django.test import Client, TestCase
from base.models import Project


class TestProject(TestCase):
	def testProjectShouldContainValidChars(self):
		# When
		response = Client().post('/ui/project', data={'name': '%letter'})
		# Then
		self.assertEqual(response.status_code, 400)

	def testProjectNameShouldBeUnder100Chars(self):
		# When
		response = Client().post('/ui/project', data={'name': 'a' * 101})
		# Then
		self.assertEqual(response.status_code, 400)

	def testProjectNameRejectIfDigitAtBegin(self):
		# When
		response = Client().post('/ui/project', data={'name': '007a'})
		# Then
		self.assertEqual(response.status_code, 400)

	def testProjectLongValidNameAreAcepted(self):
		# When
		response = Client().post('/ui/project', data={'name': 'x' * 100})
		# Then
		self.assertEqual(response.status_code, 302)		# Ok

	def testProjectShouldBeCreateOverForm(self):
		# Given
		Project.objects.all().delete()
		# When
		response = Client().post('/ui/project', data={'name': 'test_project'})
		# Then
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, '/ui')
		Project.objects.get(name='test_project')		# Not raise

	def testProjectPageHoldProjectName(self):
		# Given
		project = Project.objects.create(name='named')
		# When
		response = Client().get('/ui/project/%u/' % project.id)
		# Then
		self.assertEqual(response.status_code, 200)
		self.assertIn('named', response.content.decode('utf-8'))

	def testProjectPageContainReportUploadForm(self):
		# Given
		project = Project.objects.create()
		# When
		response = Client().get('/ui/project/%u/' % project.id)
		# Then
		self.assertEqual(response.status_code, 200)
		content = response.content.decode('utf-8')
		self.assertIn(
			"<form action='/import/' method='post' enctype='multipart/form-data'>",
			content)
		self.assertIn(
			"<input type='hidden' name='project' value='%s'>" % project.name,
			content)
