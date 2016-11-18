from django.test import RequestFactory, TestCase
from base.models import Project
from ui.views import RevisionView


class RevisionViewUT(RevisionView):
	def getRepository(self, project, revision):
		class FakeRepository:
			def head(self):
				return revision

			def prev(self):
				return '1f8b852'
		return FakeRepository()


class TestRevisionView(TestCase):
	def setUp(self):
		self.factory = RequestFactory()
		self.view = RevisionViewUT.as_view()

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
