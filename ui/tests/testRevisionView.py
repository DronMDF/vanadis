from django.test import RequestFactory, TestCase
from base.models import Project
from ui.views import RevisionView
from . import FakeRepository, FakeFile


class RevisionViewUT(RevisionView):
	repo = None

	def getRepository(self, project, revision=None):
		return self.repo


class TestRevisionView(TestCase):
	def setUp(self):
		Project.objects.create(name='project')
		self.factory = RequestFactory()
		files = [FakeFile('readme.md'), FakeFile('ui/views/RevisionView.py')]
		repo = FakeRepository('1f8b852', '67c47e6', files=files)
		self.view = RevisionViewUT.as_view(repo=repo)

	def testPageShowPreviousUrl(self):
		# Given
		request = self.factory.get('/project/67c47e6')
		# When
		response = self.view(request, projectname='project', revision='67c47e6')
		# Then
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context_data['previous'], '1f8b852')

	def testNotHeadRevisionShowPreviousUrl(self):
		# Given
		request = self.factory.get('/project/67c47e6')
		# When
		response = self.view(request, projectname='project', revision='67c47e6')
		# Then
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context_data['revision'], '67c47e6')

	def testXmlReturned(self):
		# Given
		request = self.factory.get('/project/67c47e6')
		# When
		response = self.view(request, projectname='project', revision='67c47e6')
		# Then
		self.assertEqual(response.status_code, 200)
		content = response.render().content.decode('utf8')
		self.assertIn('<?xml version="1.0" encoding="UTF-8"?>', content)

	def testXmlFilelist(self):
		# Given
		request = self.factory.get('/project/67c47e6')
		# When
		response = self.view(request, projectname='project', revision='67c47e6')
		# Then
		self.assertEqual(response.status_code, 200)
		content = response.render().content.decode('utf8')
		self.assertIn('<path>readme.md</path>', content)
		self.assertIn('<path>ui/views/RevisionView.py</path>', content)
