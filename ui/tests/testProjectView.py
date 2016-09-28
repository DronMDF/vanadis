from django.test import Client, TestCase
from base.models import File, Issue, Project


class TestProjectView(TestCase):
	def testSettingsUrl(self):
		# Given
		Project.objects.all().delete()
		Project.objects.create(name='setp')
		# When
		reply = Client().get('/setp')
		# Then
		self.assertEqual(reply.status_code, 200)
		self.assertIn("href='/setp/settings'", reply.content.decode('utf-8'))

	def testImportUrl(self):
		# Given
		Project.objects.all().delete()
		Project.objects.create(name='imp')
		# When
		reply = Client().get('/imp')
		# Then
		self.assertEqual(reply.status_code, 200)
		self.assertIn("href='/imp/import'", reply.content.decode('utf-8'))

	def testProjectPageHoldProjectName(self):
		# Given
		name = 'name-of-project'
		Project.objects.create(name=name)
		# When
		response = Client().get('/%s' % name)
		# Then
		self.assertEqual(response.status_code, 200)
		self.assertIn(name, response.content.decode('utf-8'))

	def testProjectPageContainReportUploadUrl(self):
		# Given
		name = 'name-of-project'
		Project.objects.create(name=name)
		# When
		response = Client().get('/%s' % name)
		# Then
		self.assertEqual(response.status_code, 200)
		self.assertIn('/%s/import' % name, response.content.decode('utf-8'))

	def testProjectPageContainListOfFiles(self):
		# Given
		project = Project.objects.create(name='flist')
		test1 = File.objects.create(project=project, path='test1.c')
		xen = File.objects.create(project=project, path='xeh.h')
		Issue.objects.create(project=project, file=test1, line=0, position=0)
		Issue.objects.create(project=project, file=xen, line=0, position=0)
		# When
		response = Client().get('/%s' % project.name)
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
		response = Client().get('/%s' % project.name)
		# Then
		content = response.content.decode('utf-8')
		self.assertRegex(content, 'test1.c[^2]+1')
		self.assertRegex(content, 'xeh.h[^1]+2')
