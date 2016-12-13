from django.test import Client, RequestFactory, TestCase
from base.models import File, Issue, Project
from ui.views import ProjectView
from . import FakeCommit, FakeRepository, FakeTree


class ProjectViewUT(ProjectView):
	repo = None

	def getRepository(self, project):
		return self.repo


class TestProjectView(TestCase):
	def setUp(self):
		self.factory = RequestFactory()

	def testSettingsUrl(self):
		# Given
		Project.objects.all().delete()
		Project.objects.create(name='setp')
		# When
		reply = Client().get('/setp')
		# Then
		self.assertEqual(reply.status_code, 200)
		self.assertIn("href='/setp/settings'", reply.content.decode('utf-8'))

	def testProjectPageHoldProjectName(self):
		# Given
		name = 'name-of-project'
		Project.objects.create(name=name)
		# When
		response = Client().get('/%s' % name)
		# Then
		self.assertEqual(response.status_code, 200)
		self.assertIn(name, response.content.decode('utf-8'))

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

	def testProjectPageOpenAtLastProjectRevision(self):
		# Given
		Project.objects.create(name='last')
		request = self.factory.get('/last')
		repo = FakeRepository(FakeCommit('67c47e6', FakeTree(None)))
		view = ProjectViewUT.as_view(repo=repo)
		# When
		response = view(request, projectname='last')
		# Then
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, '/last/67c47e6')
