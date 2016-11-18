from django.test import RequestFactory, TestCase
from base.models import Project
from ui.views import RevisionView
from . import FakeRepository


class RevisionViewUT(RevisionView):
	repo = None

	def getRepository(self, project, revision=None):
		return self.repo


class TestRevisionView(TestCase):
	def setUp(self):
		self.factory = RequestFactory()
		self.view = RevisionViewUT.as_view(repo=FakeRepository('1f8b852', '67c47e6'))

	def testPageShowPreviousUrl(self):
		# Given
		Project.objects.create(name='project')
		request = self.factory.get('/project/67c47e6')
		# When
		response = self.view(request, projectname='project', revision='67c47e6')
		# Then
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context_data['previous'], '1f8b852')

	def testNotHeadRevisionShowPreviousUrl(self):
		# Given
		Project.objects.create(name='project')
		request = self.factory.get('/project/67c47e6')
		# When
		response = self.view(request, projectname='project', revision='67c47e6')
		# Then
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context_data['revision'], '67c47e6')
