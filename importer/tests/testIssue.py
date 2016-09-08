from django.test import TestCase
from importer.issue import *


class TestIssueChain(TestCase):
	def testIgnoreSplitLogToChain(self):
		# Given
		log = [b'header',
			b'a.c:1:3: warning: msg', b'code', b'note',
			b'b.c:5:7: warning: xxx', b'dummy']
		# When
		result = list(splitReportToIssueChain(log))
		self.assertListEqual(result, [[b'header'],
			[b'a.c:1:3: warning: msg', b'code', b'note'],
			[b'b.c:5:7: warning: xxx', b'dummy']])
