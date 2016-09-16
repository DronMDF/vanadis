from django.test import Client, TestCase
from base.models import File, Issue, Project


class TestProject(TestCase):
	def testProjectShouldContainValidChars(self):
		# When
		response = Client().post('/ui/project', data={'name': '%letter'})
		# Then
		self.assertEqual(response.status_code, 200)

	def testProjectNameShouldBeUnder100Chars(self):
		# When
		response = Client().post('/ui/project', data={'name': 'a' * 101})
		# Then
		self.assertEqual(response.status_code, 200)

	def testProjectNameRejectIfDigitAtBegin(self):
		# When
		response = Client().post('/ui/project', data={'name': '007a'})
		# Then
		self.assertEqual(response.status_code, 200)

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
		self.assertEqual(response.url, '/ui/project/test_project')
		Project.objects.get(name='test_project')		# Not raise

	def testProjectPageHoldProjectName(self):
		# Given
		name = 'name-of-project'
		Project.objects.create(name=name)
		# When
		response = Client().get('/ui/project/%s/' % name)
		# Then
		self.assertEqual(response.status_code, 200)
		self.assertIn(name, response.content.decode('utf-8'))

	def testProjectPageContainReportUploadUrl(self):
		# Given
		name = 'name-of-project'
		Project.objects.create(name=name)
		# When
		response = Client().get('/ui/project/%s/' % name)
		# Then
		self.assertEqual(response.status_code, 200)
		content = response.content.decode('utf-8')
		self.assertIn('/ui/project/%s/import' % name, response.content.decode('utf-8'))

	def testProjectPageContainListOfFiles(self):
		# Given
		project = Project.objects.create(name='flist')
		test1 = File.objects.create(project=project, path='test1.c')
		xen = File.objects.create(project=project, path='xeh.h')
		Issue.objects.create(project=project, file=test1, line=0, position=0)
		Issue.objects.create(project=project, file=xen, line=0, position=0)
		# When
		response = Client().get('/ui/project/%s/' % project.name)
		# Then
		content = response.content.decode('utf-8')
		self.assertIn('test1.c', content)
		self.assertIn('xeh.h', content)

	def testProjectPageContainListOfFilesWithCountsOfIssue(self):
		# Given
		project = Project.objects.create(name='flist')
		test1 = File.objects.create(project=project, path='test1.c')
		xen = File.objects.create(project=project, path='xeh.h')
		Issue.objects.create(project=project, file=test1, line=0, position=0)
		Issue.objects.create(project=project, file=xen, line=0, position=0)
		Issue.objects.create(project=project, file=xen, line=1, position=0)
		# When
		response = Client().get('/ui/project/%s/' % project.name)
		# Then
		content = response.content.decode('utf-8')
		self.assertRegex(content, 'test1.c[^2]+1')
		self.assertRegex(content, 'xeh.h[^1]+2')
