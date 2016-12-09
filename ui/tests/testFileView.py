from django.test import RequestFactory, TestCase
from base.models import File, Issue, Project
from ui.tests import PredefinedFakeRepository
from ui.views import FileView


class FileViewUT(FileView):
	repo = None

	def getRepository(self, project, revision=None):
		return self.repo


class TestFileView(TestCase):
	def setUp(self):
		repo = PredefinedFakeRepository()
		self.view = FileViewUT.as_view(repo=repo)
		self.factory = RequestFactory()
		self.project = Project.objects.create(name='project')

	def testViewShouldReturnByLineContext(self):
		# Given
		xxx = File.objects.create(project=self.project, path='readme.md')
		Issue.objects.create(project=self.project, file=xxx,
				line=7, position=5, text='All bad')
		Issue.objects.create(project=self.project, file=xxx,
				line=7, position=10, text='End bad')
		request = self.factory.get('/project/67c47e6/readme.md')
		# When
		response = self.view(request, projectname='project', revision='67c47e6',
				filename='readme.md')
		# Then
		sc = response.context_data['sourcecode']
		self.assertEqual(sc[0]['line'], 7)
		self.assertEqual(sc[0]['issues'][0]['position'], 10)
		self.assertEqual(sc[0]['issues'][1]['position'], 5)

	def testDirectoryView(self):
		# Given
		request = self.factory.get('/project/67c47e6/ui')
		# When
		response = self.view(request, projectname='project', revision='67c47e6',
				filename='ui')
		# Then
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context_data['previous'], '1f8b852')

	def testDirectoryViewEntry(self):
		# Given
		request = self.factory.get('/project/67c47e6/ui')
		# When
		response = self.view(request, projectname='project', revision='67c47e6',
				filename='ui')
		# Then
		self.assertEqual(response.status_code, 200)
		content = response.render().content.decode('utf8')
		self.assertIn('<base_path>ui</base_path>', content)
		self.assertIn('<name>views</name>', content)
