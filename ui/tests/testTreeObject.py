from django.test import TestCase
from importer import RepositoryTreeObject
from ui import TreeObject
from ui.tests import FakeTree, FakeFile


class TestTreeObject(TestCase):
	def testObjectIsDir(self):
		# Given
		tree = [RepositoryTreeObject(FakeFile('this'), 'not'),
			RepositoryTreeObject(FakeTree('this'), 'is')]
		# When
		obj = TreeObject(tree, 'is/this')
		# Then
		self.assertTrue(obj.is_dir())

	def testObjectIsNotDir(self):
		# Given
		tree = [RepositoryTreeObject(FakeFile('this'), 'is'),
			RepositoryTreeObject(FakeTree('this'), 'not')]
		# When
		obj = TreeObject(tree, 'is/this')
		# Then
		self.assertFalse(obj.is_dir())

	def testObjectNotInTree(self):
		# Given
		tree = [RepositoryTreeObject(FakeFile('this'), 'is'),
			RepositoryTreeObject(FakeTree('this'), 'again')]
		# When/then
		with self.assertRaises(KeyError):
			TreeObject(tree, 'is/missing').is_dir()
