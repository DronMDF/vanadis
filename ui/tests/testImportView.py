from django.test import RequestFactory, TestCase
from django.http.response import Http404
from base.models import Issue, Project
from ui.views import ImportView
from ui.tests import FakeRepository


class ImportViewUT(ImportView):
	repo = None

	def getRepository(self, project, revision=None):
		return self.repo


class TestImportView(TestCase):
	def setUp(self):
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
		request = self.factory.post('/nonexist/import/12345678',
			content_type='application/xml', data='<files/>')
		# When
		with self.assertRaises(Http404):
			ImportViewUT.as_view()(request, projectname='nonexist', revision='12345678')

	def testMissingRevisionCause404(self):
		# Given
		Project.objects.create(name='norev')
		request = self.factory.post('/norev/import/12345678',
			content_type='application/xml', data='<files/>')
		# When
		with self.assertRaises(Http404):
			ImportViewUT.as_view()(request, projectname='norev', revision='12345678')

	def testImportSimpleIssues(self):
		# Given
		Project.objects.create(name='import1')
		repo = FakeRepository('11111111')
		request_body = ('<files><file><oid>123456789012</oid><path>xxx.c</path>'
			'<issue><line>123</line><message>xxx</message></issue></file></files>')
		request = self.factory.post('/import1/import/11111111',
			content_type='application/xml', data=request_body)
		# When
		ImportViewUT.as_view(repo=repo)(request, projectname='import1', revision='11111111')
		# Then
		issue = Issue.objects.filter(project__name='import1')[0]
		self.assertEqual(issue.file.path, 'xxx.c')
		self.assertEqual(issue.object.oid, 0x123456789012)
		self.assertEqual(issue.line, 123)
		self.assertEqual(issue.text, 'xxx')
