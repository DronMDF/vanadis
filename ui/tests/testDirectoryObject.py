from django.test import TestCase
from ui import DirectoryObject, RepositoryTreeObject
from ui.tests import FakeTree, FakeFile


class TestTreeObject(TestCase):
	def testRootContent(self):
		# Given
		tree = [RepositoryTreeObject(FakeFile('one'), ''),
			RepositoryTreeObject(FakeTree('two'), 'one'),
			RepositoryTreeObject(FakeTree('three'), '')]
		# When
		objs = DirectoryObject(tree)
		# Then
		paths = [o.path() for o in objs]
		self.assertIn('one', paths)
		self.assertIn('three', paths)
		self.assertNotIn('one/two', paths)

	def testiSubContent(self):
		# Given
		tree = [RepositoryTreeObject(FakeFile('one'), 'two'),
			RepositoryTreeObject(FakeTree('two'), ''),
			RepositoryTreeObject(FakeTree('three'), 'two')]
		# When
		objs = DirectoryObject(tree, 'two')
		# Then
		paths = [o.path() for o in objs]
		self.assertIn('two/one', paths)
		self.assertIn('two/three', paths)
		self.assertNotIn('two', paths)
