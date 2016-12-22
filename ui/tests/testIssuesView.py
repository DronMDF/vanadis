from django.test import Client, RequestFactory, TestCase
from base.models import Project
from ui.views import IssuesView
from ui.tests import PredefinedFakeRepository


class IssuesViewUT(IssuesView):
	repo = None

	def getRepository(self, project):
		return self.repo


class TestIssuesView(TestCase):
	def setUp(self):
		repository = PredefinedFakeRepository()
		self.view = IssuesViewUT.as_view(repo=repository)
		self.factory = RequestFactory()

	def testNoProject(self):
		# When
		response = Client().get('/nonexist/issues/1234567')
		# Then
		self.assertEqual(response.status_code, 404)

	def testXmlMainTag(self):
		# Given
		project = Project.objects.create(name='xml')
		self.addCleanup(project.delete)
		request = self.factory.get('/xml/issues/67c47e6')
		# When
		response = self.view(request, projectname='xml', revision='67c47e6')
		# Then
		self.assertEqual(response.status_code, 200)
		content = response.render().content.decode('utf8')
		self.assertIn('<issues>', content)
		self.assertIn('</issues>', content)