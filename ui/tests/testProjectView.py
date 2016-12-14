from django.test import RequestFactory, TestCase
from base.models import Project
from ui.views import ProjectView
from . import PredefinedFakeRepository


class ProjectViewUT(ProjectView):
	repo = None

	def getRepository(self, project):
		return self.repo


class TestProjectView(TestCase):
	def setUp(self):
		self.factory = RequestFactory()

	def testProjectPageOpenAtLastProjectRevision(self):
		# Given
		Project.objects.create(name='last')
		request = self.factory.get('/last')
		view = ProjectViewUT.as_view(repo=PredefinedFakeRepository())
		# When
		response = view(request, projectname='last')
		# Then
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, '/last/67c47e6')
