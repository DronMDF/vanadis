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

	def __init__(self, name, oid='123456789012', content=None):
		self.name = name
		self.id = FakeOid(oid)
		content = list() if content is None else content
		self.data = '\n'.join(content).encode('utf8')


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
	def __init__(self, tree, repo):
		self.tree = tree
		self.repo = repo

	def getTreeFiles(self, tree, prefix):
		for te in tree.files:
			filename = str(Path(prefix, te.name))
			yield RepositoryTreeObject(te, prefix, self.repo)
			if isinstance(te, FakeTree):
				yield from self.getTreeFiles(te, filename)

	def __iter__(self):
		yield from self.getTreeFiles(self.tree, '')


class FakeRepository:
	def __init__(self, *commits):
		''' commits are log ordered (from newest) FakeCommit '''
		self.commits = commits

	def __getitem__(self, oid):
		for c in self.commits:
			for f in self.tree(c.revision):
				if str(f.id()) == str(oid):
					return f.entry
		raise KeyError(oid)

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
				return FakeTreeList(c.tree, self)
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
				FakeFile('readme.md', oid='9c0398b0dbf6'),
				FakeTree('ui',
					FakeTree('views',
						FakeFile('RevisionView.py', oid='bfc51f6ed870',
							content=['line1', 'line2', 'line3']))))),
			FakeCommit('1f8b852', FakeTree(None)))
