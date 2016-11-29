from django.test import RequestFactory, TestCase
from django.http.response import Http404
from base.models import Issue, Project
from ui.views import ImportView
from ui.tests import FakeFile, FakeRepository


class ImportViewUT(ImportView):
	repo = None

	def getRepository(self, project, revision=None):
		return self.repo


class TestImportView(TestCase):
	def setUp(self):
		repository = FakeRepository(
			commits=['88abd8249ee8'],
			files=[
				FakeFile('README', '09f34f78f2bb6ab5'),
				FakeFile('arch/mips/Makefile', '1a6bac7b076f31934d')
			]
		)
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
		request = self.factory.post('/nonexist/import/12345678',
			content_type='application/xml', data='<files/>')
		# When
		with self.assertRaises(Http404):
			self.view(request, projectname='nonexist', revision='12345678')

	def testMissingRevisionCause404(self):
		# Given
		Project.objects.create(name='norev')
		request = self.factory.post('/norev/import/12345678',
			content_type='application/xml', data='<files/>')
		# When
		with self.assertRaises(Http404):
			self.view(request, projectname='norev', revision='12345678')

	def testImportSimpleIssues(self):
		# Given
		Project.objects.create(name='import1')
		request_body = ('<files><file><oid>123456789012</oid><path>xxx.c</path>'
			'<issue><line>123</line><message>xxx</message></issue></file></files>')
		request = self.factory.post('/import1/import/88abd82',
			content_type='application/xml', data=request_body)
		# When
		self.view(request, projectname='import1', revision='88abd82')
		# Then
		issue = Issue.objects.filter(project__name='import1')[0]
		self.assertEqual(issue.file.path, 'xxx.c')
		self.assertEqual(issue.object.oid, 0x123456789012)
		self.assertEqual(issue.line, 123)
		self.assertEqual(issue.text, 'xxx')
