from django.test import TestCase
from ui import RepositoryHistory
from ui.tests import FakeCommit, FakeCommitChain, FakeTree


class TestRepositoryHistory(TestCase):
	def testEmptyHistoryIsUnlimited(self):
		# Given
		hist = RepositoryHistory(None)
		# When
		hi = iter(hist)
		# Then
		self.assertEqual(str(next(hi).id())[:7], '0000000')
		self.assertEqual(str(next(hi).id())[:7], '0000000')
		self.assertEqual(str(next(hi).id())[:7], '0000000')

	def testEmptyHistory(self):
		# Given
		head = FakeCommitChain(
			FakeCommit('67c47e6', FakeTree(None)),
			FakeCommit('1f8b852', FakeTree(None)))
		hist = RepositoryHistory(head)
		# When
		hi = iter(hist)
		# Then
		self.assertEqual(str(next(hi).id())[:7], '67c47e6')
		self.assertEqual(str(next(hi).id())[:7], '1f8b852')
		self.assertEqual(str(next(hi).id())[:7], '0000000')
