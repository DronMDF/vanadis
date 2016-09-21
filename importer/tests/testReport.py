import string
import random
import time
from django.test import TestCase
from importer.Report import Report


class TestReport(TestCase):
	def testParseSimpleClangReport(self):
		# Given
		report = Report('\n'.join([
			'pid_output.c:101:30: warning: implicit conversion',
			'    else if (ftruncate(fd, pidsize) < 0)']))
		# When
		files = list(report.files())
		# Then
		self.assertListEqual(files, ['pid_output.c'])

	def testReportAllowIterateOverIssues(self):
		# Given
		report = Report('\n'.join([
			'pid_output.c:101:30: warning: implicit conversion',
			'    else if (ftruncate(fd, pidsize) < 0)']))
		# When
		issue = next(report.issues())
		# Then
		self.assertEqual(issue.file, 'pid_output.c')
		self.assertEqual(issue.line, 101)
		self.assertEqual(issue.position, 30)
		self.assertEqual(issue.message, 'implicit conversion')
		self.assertEqual(issue.code, '    else if (ftruncate(fd, pidsize) < 0)')

	def testReportShouldCutDitsFromPath(self):
		# Given
		report = Report('\n'.join([
			'dir/pid_output.c:101:30: warning: implicit conversion',
			'    else if (ftruncate(fd, pidsize) < 0)',
			'./in/pid_output.c:101:30: warning: implicit conversion',
			'    else if (ftruncate(fd, pidsize) < 0)',
			'../pid_output.c:101:30: warning: implicit conversion',
			'    else if (ftruncate(fd, pidsize) < 0)']))
		# When
		files = list(report.files())
		# Then
		self.assertIn('dir/pid_output.c', files)
		self.assertIn('in/pid_output.c', files)
		self.assertIn('pid_output.c', files)


class TestReportPerformance(TestCase):
	def generateKiloReport(self):
		def rs(size, extra_chars=''):
			charset = string.ascii_letters + string.digits + extra_chars
			return ''.join(random.choice(charset) for _ in range(size))

		def rl():
			return '%s:%u:%u: warning: %s\n%s' % (rs(30, '/'), random.randint(1, 10000),
				random.randint(1, 300), rs(80, ' '), rs(300, string.punctuation))
		return '\n'.join(rl() for _ in range(1000))

	def setUp(self):
		self.report_text = self.generateKiloReport()
		self.start_time = time.time()

	def tearDown(self):
		delta = time.time() - self.start_time
		self.assertLess(delta, 0.05)

	def testKiloIssuesParsing(self):
		# When
		report = Report(self.report_text)
		# Then
		self.assertGreater(len(list(report.files())), 0)
		self.assertGreater(len(list(report.issues())), 0)
