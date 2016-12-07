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


class FakeTree:
	def __init__(self, name, *files):
		self.id = FakeOid('123456789012')
		self.name = name
		self.files = files


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
			if isinstance(te, FakeTree) and recursive:
				yield from self.getTreeFiles(te, filename, recursive)
			else:
				File = namedtuple('File', ['id', 'path'])
				yield File(te.id, filename)

	def getFiles(self, revision, recursive):
		for c in self.commits:
			if c.revision == revision:
				yield from self.getTreeFiles(c.tree, '', recursive)
