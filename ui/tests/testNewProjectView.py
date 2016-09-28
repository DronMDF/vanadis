from django.test import Client, TestCase
from base.models import Project


class TestNewProjectView(TestCase):
	def testAction(self):
		# When
		reply = Client().get('/newproject')
		# Then
		self.assertEqual(reply.status_code, 200)
		self.assertIn("action='/newproject'", reply.content.decode('utf8'))

	def testProjectShouldContainValidChars(self):
		# When
		response = Client().post('/newproject', data={'name': '%letter'})
		# Then
		self.assertEqual(response.status_code, 200)

	def testProjectNameShouldBeUnder100Chars(self):
		# When
		response = Client().post('/newproject', data={'name': 'a' * 101})
		# Then
		self.assertEqual(response.status_code, 200)

	def testProjectNameRejectIfDigitAtBegin(self):
		# When
		response = Client().post('/newproject', data={'name': '007a'})
		# Then
		self.assertEqual(response.status_code, 200)

	def testProjectLongValidNameAreAcepted(self):
		# When
		response = Client().post('/newproject', data={'name': 'x' * 100})
		# Then
		self.assertEqual(response.status_code, 302)		# Ok

	def testProjectShouldBeCreateOverForm(self):
		# Given
		Project.objects.all().delete()
		# When
		response = Client().post('/newproject', data={'name': 'test_project'})
		# Then
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, '/test_project')
		Project.objects.get(name='test_project')		# Not raise

	def testT2IsCorrectProjectName(self):
		# When
		response = Client().post('/newproject', data={'name': 't2'})
		# Then
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, '/t2')
		Project.objects.get(name='t2')		# Not raise
