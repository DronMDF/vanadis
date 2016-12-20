from django.test import RequestFactory, TestCase
from django.http.response import Http404
from base.models import Issue, Project
from ui.views import ImportView
from ui.tests import PredefinedFakeRepository


class ImportViewUT(ImportView):
	repo = None

	def getRepository(self, project):
		return self.repo


class TestImportView(TestCase):
	def setUp(self):
		repository = PredefinedFakeRepository()
		self.view = ImportViewUT.as_view(repo=repository)
		self.factory = RequestFactory()

	def testXmlParsing(self):
		# Given
		from xml.etree import ElementTree
		request_body = ('<files><file><path>xxx.c</path>'
			'<issue><line>123</line><message>xxx</message></issue></file></files>')
		it = ElementTree.fromstring(request_body)
		# When
		issue = it.findall('./file')
		# Then
		self.assertEqual(len(issue), 1)

	def testMissingProjectCause404(self):
		# Given
		request = self.factory.post('/nonexist/import/1234567',
			content_type='application/xml', data='<files/>')
		# When
		with self.assertRaises(Http404):
			self.view(request, projectname='nonexist', revision='1234567')

	def testMissingRevisionCause404(self):
		# Given
		project = Project.objects.create(name='norev')
		self.addCleanup(project.delete)
		request = self.factory.post('/norev/import/1234567',
			content_type='application/xml', data='<files/>')
		# When
		with self.assertRaises(Http404):
			self.view(request, projectname='norev', revision='1234567')

	def testImportSimpleIssues(self):
		# Given
		project = Project.objects.create(name='import1')
		self.addCleanup(project.delete)
		# first 6 bytes of bfc51f6ed870 in b64 is a 'v8Ufbthw'
		request_body = ('<files><file><id>v8Ufbthw</id>'
			'<issue><line>123</line><message>xxx</message></issue></file></files>')
		request = self.factory.post('/import1/import/67c47e6',
			content_type='application/xml', data=request_body)
		# When
		self.view(request, projectname='import1', revision='67c47e6')
		# Then
		issue = Issue.objects.filter(project__name='import1')[0]
		self.assertEqual(issue.object.oid, 0xbfc51f6ed870)
		self.assertEqual(issue.line, 123)
		self.assertEqual(issue.text, 'xxx')
