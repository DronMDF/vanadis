import io
import random
import string
import time
from django.test import TestCase
from importer.Report import Report


class TestReport(TestCase):
	def testParseSimpleClangReport(self):
		# Given
		report_text = '\n'.join(('pid_output.c:101:30: warning: implicit conversion',
			'    else if (ftruncate(fd, pidsize) < 0)'))
		report = Report(io.StringIO(report_text))
		# When
		files = list(report.files())
		# Then
		self.assertListEqual(files, ['pid_output.c'])

	def testReportAllowIterateOverIssues(self):
		# Given
		report_text = '\n'.join(('pid_output.c:101:30: warning: implicit conversion',
			'    else if (ftruncate(fd, pidsize) < 0)'))
		report = Report(io.StringIO(report_text))
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
		report_text = '\n'.join([
			'dir/pid_output.c:101:30: warning: implicit conversion',
			'    else if (ftruncate(fd, pidsize) < 0)',
			'./in/pid_output.c:101:30: warning: implicit conversion',
			'    else if (ftruncate(fd, pidsize) < 0)',
			'../pid_output.c:101:30: warning: implicit conversion',
			'    else if (ftruncate(fd, pidsize) < 0)'])
		report = Report(io.StringIO(report_text))
		# When
		files = set(report.files())
		# Then
		self.assertSetEqual(files, {'dir/pid_output.c', 'in/pid_output.c'})

	def testParseCppcheckWarning(self):
		# Given
		report_text = ("[bgpd/bgp_aspath.c:1867] -> [bgpd/bgp_aspath.c:1865]:"
			" (warning) Either the condition 'seg2' is redundant or there"
			" is possible null pointer dereference: seg2.")
		report = Report(io.StringIO(report_text))
		# When
		files = list(report.files())
		issues = list(report.issues())
		# Then
		self.assertListEqual(files, ['bgpd/bgp_aspath.c'])
		self.assertEqual(len(issues), 1)
		self.assertEqual(issues[0].file, 'bgpd/bgp_aspath.c')
		self.assertEqual(issues[0].line, 1867)
		self.assertEqual(issues[0].message, ("Either the condition 'seg2' "
			"is redundant or there is possible null pointer dereference: seg2."))

	def testParseCppcheckStyle(self):
		# Given
		report_text = ("[bgpd/bgp_aspath.c:147]: (style) "
			"The scope of the variable 'prev' can be reduced.")
		report = Report(io.StringIO(report_text))
		# When
		files = list(report.files())
		issues = list(report.issues())
		# Then
		self.assertListEqual(files, ['bgpd/bgp_aspath.c'])
		self.assertEqual(len(issues), 1)
		self.assertEqual(issues[0].file, 'bgpd/bgp_aspath.c')
		self.assertEqual(issues[0].line, 147)
		self.assertEqual(issues[0].message,
			"The scope of the variable 'prev' can be reduced.")

	def testParseCppcheckError(self):
		# Given
		report_text = ("[bgpd/bgp_route.c:358]: "
			"(error) Uninitialized struct member: newattr.extra")
		report = Report(io.StringIO(report_text))
		# When
		files = list(report.files())
		issues = list(report.issues())
		# Then
		self.assertListEqual(files, ['bgpd/bgp_route.c'])
		self.assertEqual(len(issues), 1)
		self.assertEqual(issues[0].file, 'bgpd/bgp_route.c')
		self.assertEqual(issues[0].line, 358)
		self.assertEqual(issues[0].message,
			"Uninitialized struct member: newattr.extra")

	def testParseCppcheckPerformance(self):
		# Given
		report_text = ("[ripngd/ripngd.c:2101] -> [ripngd/ripngd.c:2108]: "
			"(performance) Variable 'len' is reassigned a value "
			"before the old one has been used.")
		report = Report(io.StringIO(report_text))
		# When
		files = list(report.files())
		issues = list(report.issues())
		# Then
		self.assertListEqual(files, ['ripngd/ripngd.c'])
		self.assertEqual(len(issues), 1)
		self.assertEqual(issues[0].file, 'ripngd/ripngd.c')
		self.assertEqual(issues[0].line, 2101)
		self.assertEqual(issues[0].message,
			"Variable 'len' is reassigned a value before the old one has been used.")

	def testParseCppcheckInformationIsNotIssue(self):
		# Given
		report_text = ("[./bgpd/bgp_main.c:1]: (information) "
			"Skipping configuration 'QUAGGA_GROUP;QUAGGA_USER'")
		report = Report(io.StringIO(report_text))
		# Then
		self.assertListEqual(list(report.files()), [])
		self.assertListEqual(list(report.issues()), [])


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
		self.assertLess(delta, 0.5)

	def testKiloIssuesParsing(self):
		# When
		report = Report(io.StringIO(self.report_text))
		# Then
		self.assertGreater(len(list(report.files())), 0)
		self.assertGreater(len(list(report.issues())), 0)
