from django.test import RequestFactory, TestCase
from django.http.response import Http404
from base.models import Issue, Project
from ui.views import ImportView
from ui.tests import FakeCommit, FakeFile, FakeRepository, FakeTree


class ImportViewUT(ImportView):
	repo = None

	def getRepository(self, project):
		return self.repo


class TestImportView(TestCase):
	def setUp(self):
		repository = FakeRepository(
			FakeCommit('88abd8249ee8', FakeTree(None,
				FakeFile('README', '09f34f78f2bb6ab5'),
				FakeTree('arch',
					FakeTree('mips',
						FakeFile('Makefile', '1a6bac7b076f31934d'))))))
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
		project = Project.objects.create(name='norev')
		self.addCleanup(project.delete)
		request = self.factory.post('/norev/import/12345678',
			content_type='application/xml', data='<files/>')
		# When
		with self.assertRaises(Http404):
			self.view(request, projectname='norev', revision='12345678')

	def testImportSimpleIssues(self):
		# Given
		project = Project.objects.create(name='import1')
		self.addCleanup(project.delete)
		# first 6 bytes of 1a6bac7b076f31934d in b64 is a 'Gmusewdv'
		request_body = ('<files><file><id>Gmusewdv</id>'
			'<issue><line>123</line><message>xxx</message></issue></file></files>')
		request = self.factory.post('/import1/import/88abd82',
			content_type='application/xml', data=request_body)
		# When
		self.view(request, projectname='import1', revision='88abd82')
		# Then
		issue = Issue.objects.filter(project__name='import1')[0]
		self.assertEqual(issue.object.oid, 0x1a6bac7b076f31)
		self.assertEqual(issue.line, 123)
		self.assertEqual(issue.text, 'xxx')
