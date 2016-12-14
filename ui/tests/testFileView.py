from django.test import RequestFactory, TestCase
from base.models import Issue, Object, Project
from ui import RepositoryId
from ui.tests import FakeOid, PredefinedFakeRepository
from ui.views import FileView


class FileViewUT(FileView):
	repo = None

	def getRepository(self, project):
		return self.repo


class TestFileView(TestCase):
	def setUp(self):
		repo = PredefinedFakeRepository()
		self.view = FileViewUT.as_view(repo=repo)
		self.factory = RequestFactory()
		self.project = Project.objects.create(name='project')

	def testViewShouldReturnByLineContext(self):
		# Given
		xxx = Object.objects.create(project=self.project,
				oid=RepositoryId(FakeOid('bfc51f6ed870')).int(), issues_count=0)
		Issue.objects.create(project=self.project, object=xxx,
				line=2, position=5, text='All bad')
		Issue.objects.create(project=self.project, object=xxx,
				line=2, position=10, text='End bad')
		request = self.factory.get('/project/67c47e6/ui/views/RevisionView.py')
		# When
		response = self.view(request, projectname='project', revision='67c47e6',
				filename='ui/views/RevisionView.py')
		# Then
		sc = response.context_data['lines']
		self.assertEqual(sc[1]['lineno'], 2)
		self.assertIn(5, (i['position'] for i in sc[1]['issues']))
		self.assertIn(10, (i['position'] for i in sc[1]['issues']))

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

	def testFileViewEntry(self):
		# Given
		request = self.factory.get('/project/67c47e6/ui/views/RevisionView.py')
		# When
		response = self.view(request, projectname='project', revision='67c47e6',
				filename='ui/views/RevisionView.py')
		# Then
		self.assertEqual(response.status_code, 200)
		content = response.render().content.decode('utf8')
		self.assertIn('<revision>67c47e6</revision>', content)
		self.assertIn('<path>ui/views/RevisionView.py</path>', content)

	def testFileViewContent(self):
		# Given
		request = self.factory.get('/project/67c47e6/ui/views/RevisionView.py')
		# When
		response = self.view(request, projectname='project', revision='67c47e6',
				filename='ui/views/RevisionView.py')
		# Then
		self.assertEqual(response.status_code, 200)
		content = response.render().content.decode('utf8')
		self.assertIn('<code>line1</code>', content)
		self.assertIn('<code>line2</code>', content)
		self.assertIn('<code>line3</code>', content)
