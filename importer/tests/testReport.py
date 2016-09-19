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
