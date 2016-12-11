from binascii import hexlify, unhexlify
from pathlib import Path
from importer import RepositoryTreeObject


class FakeOid:
	def __init__(self, oid):
		self.raw = unhexlify(oid)

	def __str__(self):
		return hexlify(self.raw).decode('ascii')


class FakeFile:
	type = 'blob'

	def __init__(self, name, oid='123456789012'):
		self.name = name
		self.id = FakeOid(oid)


class FakeTree:
	type = 'tree'

	def __init__(self, name, *files):
		self.id = FakeOid('123456789012')
		self.name = name
		self.files = files


class FakeCommit:
	def __init__(self, revision, tree):
		self.revision = revision
		self.tree = tree


class FakeTreeList:
	def __init__(self, tree):
		self.tree = tree

	def getTreeFiles(self, tree, prefix):
		for te in tree.files:
			filename = str(Path(prefix, te.name))
			yield RepositoryTreeObject(te, prefix)
			if isinstance(te, FakeTree):
				yield from self.getTreeFiles(te, filename)

	def __iter__(self):
		yield from self.getTreeFiles(self.tree, '')


class FakeRepository:
	def __init__(self, *commits):
		''' commits are log ordered (from newest) FakeCommit '''
		self.commits = commits

	def revparse(self, revision):
		for c in self.commits:
			if c.revision.startswith(revision):
				return c.revision
		raise KeyError(revision)

	def head(self):
		return self.commits[0].revision

	def prev(self):
		return self.commits[1].revision

	def tree(self, revision):
		for c in self.commits:
			if c.revision == revision:
				return FakeTreeList(c.tree)
		raise KeyError(revision)

	def getFile(self, hid):
		''' TODO: Move to filter '''
		for f in self.tree(self.commits[0].revision):
			if str(f.id()).startswith(hid):
				return f
		raise KeyError(hid)


class PredefinedFakeRepository(FakeRepository):
	def __init__(self):
		super().__init__(
			FakeCommit('67c47e6', FakeTree(None,
				FakeFile('readme.md', '9c0398b0dbf6'),
				FakeTree('ui',
					FakeTree('views',
						FakeFile('RevisionView.py', 'bfc51f6ed870'))))),
			FakeCommit('1f8b852', FakeTree(None)))
