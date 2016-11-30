import io
import random
import string
import time
from django.test import TestCase
from base.models import File, Issue, Project
from importer.Report import Report
from importer.ReportStorage import ReportStorage


class TestIssue:
	def __init__(self, file, line=77, position=88, message='Wow'):
		self.file = file
		self.line = line
		self.position = position
		self.message = message


class TestReport(Report):
	def __init__(self, issues):		# pylint: disable=super-init-not-called
		self._issues = list(issues)
		self._files = set((i.file for i in self._issues))


class TestReportStorage(TestCase):
	def testStorageShouldCreateMissiongFiles(self):
		# Given
		project = Project.objects.create(name='test')
		File.objects.create(project=project, path='file1')
		storage = ReportStorage(project)
		report = TestReport([TestIssue('file1'), TestIssue('file2')])
		# When
		storage.importReport(report)
		# Then
		File.objects.get(project=project, path='file2')		# no throw

	def testStorageShouldCreateMissingIssues(self):
		# Given
		project = Project.objects.create(name='test')
		file = File.objects.create(project=project, path='file1')
		Issue.objects.create(project=project, file=file, line=10, position=20,
			text='Error')
		storage = ReportStorage(project)
		report = TestReport([
			TestIssue('file1', line=10, position=20, message='Error'),
			TestIssue('file1', line=20)])
		# When
		storage.importReport(report)
		# Then
		Issue.objects.get(project=project, file=file, line=20)		# no throw
		self.assertEqual(Issue.objects.filter(project=project, file=file).count(), 2)

	def testStorageShouldMatchingFilenamesToBig(self):
		# Given
		project = Project.objects.create(name='test')
		file = File.objects.create(project=project, path='path/to/file')
		storage = ReportStorage(project)
		report = TestReport([TestIssue('to/file')])
		# When
		storage.importReport(report)
		# Then
		self.assertEqual(Issue.objects.filter(project=project, file=file).count(), 1)

	def testStorageShouldMatchingFilenamesToShortAndUpdateFile(self):
		# Given
		project = Project.objects.create(name='test')
		file = File.objects.create(project=project, path='to/file')
		storage = ReportStorage(project)
		report = TestReport([TestIssue('path/to/file')])
		# When
		storage.importReport(report)
		# Then
		self.assertEqual(File.objects.get(pk=file.pk).path, 'path/to/file')


class TestReportStoragePerformance(TestCase):
	def generateKiloReport(self):
		def rs(size, extra_chars=''):
			charset = string.ascii_letters + string.digits + extra_chars
			return ''.join(random.choice(charset) for _ in range(size))

		def rl():
			return '%s:%u:%u: warning: %s\n%s' % (rs(30, '/'), random.randint(1, 10000),
				random.randint(1, 300), rs(80, ' '), rs(300, string.punctuation))
		return '\n'.join(rl() for _ in range(1000))

	def setUp(self):
		self.report = Report(io.StringIO(self.generateKiloReport()))
		self.start_time = time.time()

	def tearDown(self):
		delta = time.time() - self.start_time
		self.assertLess(delta, 1)

	def testKiloIssuesParsing(self):
		# Given
		project = Project.objects.create(name='test')
		storage = ReportStorage(project)
		# When
		storage.importReport(self.report)
		# Then
		self.assertEqual(Issue.objects.filter(project=project).count(), 1000)
