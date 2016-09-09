from django.test import TestCase
from importer.issue import *


class TestIssueChain(TestCase):
	def testIgnoreSplitLogToChain(self):
		# Given
		log = [
			b'header',
			b'a.c:1:3: warning: msg', b'code', b'note',
			b'b.c:5:7: warning: xxx', b'dummy']
		# When
		result = list(splitReportToIssueChain(log))
		self.assertListEqual(result, [
			[b'header'],
			[b'a.c:1:3: warning: msg', b'code', b'note'],
			[b'b.c:5:7: warning: xxx', b'dummy']])


class TestIssueRepr(TestCase):
	def testIssueReprEquality(self):
		# Given
		i1 = IssueRepr(None, './conf.h', 35, 44, 'Problem', 'nil')
		i2 = IssueRepr(None, '../conf.h', 35, 44, 'Problem', 'nil')
		# Then
		self.assertEqual(i1, i2)
