from django.test import TestCase
from ui import RepositoryTreeObject, TreeObjectsWithPathname
from ui.tests import FakeTree, FakeFile


class TestTreeObjectWithPathname(TestCase):
	def testObjectNotExist(self):
		# Given
		objs = TreeObjectsWithPathname([], 'non/exist/path')
		# When/Then
		with self.assertRaises(StopIteration):
			next(iter(objs))

	def testExistObject(self):
		# Given
		tree = [RepositoryTreeObject(FakeFile('one'), ''),
			RepositoryTreeObject(FakeTree('two'), 'one'),
			RepositoryTreeObject(FakeTree('three'), '')]
		objs = TreeObjectsWithPathname(tree, 'one/two')
		# When
		o = next(iter(objs))
		# Then
		self.assertEqual(o.path(), 'one/two')
