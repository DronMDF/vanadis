from binascii import hexlify, unhexlify
from pathlib import Path
from ui import RepositoryTreeObject


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
		self.id = revision
		self.tree = tree


class FakeCommitChain:
	def __init__(self, first_commit, *parents):
		self.id = first_commit.id
		self.tree = first_commit.tree
		if len(parents) > 0:
			self.parent_ids = [parents[0].id]
			self.parents = [FakeCommitChain(parents[0], *parents[1:])]
		else:
			self.parent_ids = []
			self.parents = []


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
		self._head = FakeCommitChain(commits[0], *commits[1:])

	def __getitem__(self, oid):
		c = self._head
		while c is not None:
			for f in self.tree(c.id):
				if str(f.id()) == str(oid):
					return f.entry
			c = next(c.parents, None)
		raise KeyError(oid)

	def revparse(self, revision):
		c = self._head
		while c is not None:
			if c.id.startswith(revision):
				return c.id
			c = next(c.parents, None)
		raise KeyError(revision)

	def head(self):
		return self._head.id

	def prev(self):
		if len(self._head.parents) > 0:
			return self._head.parents[0].id
		return None

	def tree(self, revision):
		c = self._head
		while c is not None:
			if c.id == revision:
				return FakeTreeList(c.tree, self)
			c = next(c.parents, None)
		raise KeyError(revision)

	def getFile(self, hid):
		''' TODO: Move to filter '''
		for f in self.tree(self._head.id):
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
