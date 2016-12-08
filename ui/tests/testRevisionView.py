from django.test import RequestFactory, TestCase
from base.models import Project
from ui.views import RevisionView
from . import PredefinedFakeRepository


class RevisionViewUT(RevisionView):
	repo = None

	def getRepository(self, project, revision=None):
		return self.repo


class TestRevisionView(TestCase):
	def setUp(self):
		repo = PredefinedFakeRepository()
		self.view = RevisionViewUT.as_view(repo=repo)
		self.factory = RequestFactory()
		Project.objects.create(name='project')

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
		request = self.factory.get('/project/67c47e6?view=full')
		# When
		response = self.view(request, projectname='project', revision='67c47e6',
			view='recursive')
		# Then
		self.assertEqual(response.status_code, 200)
		content = response.render().content.decode('utf8')
		self.assertIn('<path>readme.md</path>', content)
		self.assertIn('<path>ui/views/RevisionView.py</path>', content)

	def testXmlFilelistNotRecursive(self):
		# Given
		request = self.factory.get('/project/67c47e6')
		# When
		response = self.view(request, projectname='project', revision='67c47e6')
		# Then
		self.assertEqual(response.status_code, 200)
		content = response.render().content.decode('utf8')
		self.assertIn('<path>readme.md</path>', content)
		self.assertIn('<path>ui</path>', content)

	def testXmlFileOids(self):
		# Given
		request = self.factory.get('/project/67c47e6')
		# When
		response = self.view(request, projectname='project', revision='67c47e6',
			view='recursive')
		# Then
		self.assertEqual(response.status_code, 200)
		content = response.render().content.decode('utf8')
		# File id encode to base64 encoding, first 6 bytes.
		self.assertIn('<id>nAOYsNv2</id>', content)
		self.assertIn('<id>v8Ufbthw</id>', content)
