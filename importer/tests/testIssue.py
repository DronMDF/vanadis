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


class TestFileRepr(TestCase):
	def testNormalizePathDot(self):
		# Given
		f = FileRepr('./conf.h')
		# Then
		self.assertEqual(f.path, 'conf.h')

	def testNormalizePathDoubleDot(self):
		# Given
		f = FileRepr('../conf.h')
		# Then
		self.assertEqual(f.path, 'conf.h')

	def testNormalizePathWithPath(self):
		# Given
		f = FileRepr('path/conf.h')
		# Then
		self.assertEqual(f.path, 'path/conf.h')

	def testNormalizePathWithDoubleDotInMiddle(self):
		# Given
		f = FileRepr('path/a/../conf.h')
		# Then
		self.assertEqual(f.path, 'path/conf.h')

	def testNormalizePathWithDoubleSlashInMiddle(self):
		# Given
		f = FileRepr('path//conf.h')
		# Then
		self.assertEqual(f.path, 'path/conf.h')

	def testNormalizePathWithDotInMiddle(self):
		# Given
		f = FileRepr('path/./conf.h')
		# Then
		self.assertEqual(f.path, 'path/conf.h')


class TestIssueRepr(TestCase):
	def testIssueReprEquality(self):
		# Given
		f = FileRepr('conf.h')
		i1 = IssueRepr(None, f, 35, 44, 'Problem', 'nil')
		i2 = IssueRepr(None, f, 35, 44, 'Problem', 'nil')
		# Then
		self.assertEqual(i1, i2)

	def testIssueReprConvertToModel(self):
		# Given
		f = FileRepr('./conf.h')
		i = IssueRepr(None, f, 35, 44, 'Problem', 'nil')
		# When
		m = i.asModel()
		# Then
		self.assertEqual(m.file, f.path)
		self.assertEqual(m.line, i.line)
		self.assertEqual(m.position, i.position)
		self.assertEqual(m.text, i.message)
		self.assertEqual(m.code, i.code)
