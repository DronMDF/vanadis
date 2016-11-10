from django.test import RequestFactory, TestCase
from ui.views import ImportView
from base.models import Issue, Project


class ImportViewUT(ImportView):
	pass


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

	def testImportSimpleIssues(self):
		# Given
		Project.objects.create(name='import1')
		request_body = ('<files><file><path>xxx.c</path>'
			'<issue><line>123</line><message>xxx</message></issue></file></files>')
		request = self.factory.post('/import1/import/0', content_type='application/xml',
			data=request_body)
		# When
		ImportViewUT.as_view()(request, projectname='import1')
		# Then
		issue = Issue.objects.filter(project__name='import1')[0]
		self.assertEqual(issue.file.path, 'xxx.c')
		self.assertEqual(issue.line, 123)
		self.assertEqual(issue.text, 'xxx')
