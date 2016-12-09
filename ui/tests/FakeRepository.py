from binascii import hexlify, unhexlify
from collections import namedtuple
from pathlib import Path


class FakeOid:
	def __init__(self, oid):
		self.raw = unhexlify(oid)

	def __str__(self):
		return hexlify(self.raw).decode('ascii')


class FakeFile:
	def __init__(self, name, oid='0123456789012'):
		self.name = name
		self.id = FakeOid(oid)

	def is_dir(self):
		return False


class FakeTree:
	def __init__(self, name, *files):
		self.id = FakeOid('123456789012')
		self.name = name
		self.files = files

	def is_dir(self):
		return True


class FakeCommit:
	def __init__(self, revision, tree):
		self.revision = revision
		self.tree = tree


class FakeRepository:
	def __init__(self, *commits):
		''' commits are log ordered (from newest) FakeCommit '''
		self.commits = commits

	def revparse(self, revision):
		for c in self.commits:
			if c.revision.startswith(revision):
				return c.revision
		raise KeyError(revision)

	def findTreeFile(self, tree, hid):
		for te in tree.files:
			if isinstance(te, FakeFile):
				if str(te.id).startswith(hid):
					return te
			else:
				oid = self.findTreeFile(te, hid)
				if oid is not None:
					return oid
		return None

	def getFile(self, hid):
		for c in self.commits:
			oid = self.findTreeFile(c.tree, hid)
			if oid is not None:
				return oid
		raise KeyError(hid)

	def head(self):
		return self.commits[0].revision

	def prev(self):
		return self.commits[1].revision

	def getTreeFiles(self, tree, prefix, recursive):
		for te in tree.files:
			filename = str(Path(prefix, te.name))
			File = namedtuple('File', ['id', 'path', 'name'])
			yield File(te.id, filename, te.name)
			if isinstance(te, FakeTree) and recursive:
				yield from self.getTreeFiles(te, filename, recursive)

	def getFiles(self, revision, recursive=False):
		for c in self.commits:
			if c.revision == revision:
				yield from self.getTreeFiles(c.tree, '', recursive)

	def getObjectByTreePath(self, tree, prefix, path):
		for te in tree.files:
			filename = str(Path(prefix, te.name))
			if path == filename:
				return te
			if isinstance(te, FakeTree) and path.startswith(filename + '/'):
				return self.getObjectIdByPath(te, filename, path)
		raise KeyError(prefix)

	def getObjectByPath(self, revision, path):
		for c in self.commits:
			if str(c.revision).startswith(revision):
				return self.getObjectByTreePath(c.tree, '', path)
		raise KeyError(revision + '/' + path)


class PredefinedFakeRepository(FakeRepository):
	def __init__(self):
		super().__init__(
			FakeCommit('67c47e6', FakeTree(None,
				FakeFile('readme.md', '9c0398b0dbf6'),
				FakeTree('ui',
					FakeTree('views',
						FakeFile('RevisionView.py', 'bfc51f6ed870'))))),
			FakeCommit('1f8b852', FakeTree(None)))
