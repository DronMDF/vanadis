from collections import namedtuple
from pathlib import Path
import pygit2


class RepositoryObjectWrapper:
	def __init__(self, obj):
		self.id = obj.id
		self.obj = obj

	def is_dir(self):
		return self.obj.type == 2


class Repository:
	def __init__(self, project, revision=None):
		if project.repo_url is None:
			raise RuntimeError('No repository url')
		try:
			path = Path('/tmp/repos', project.name)
			if path.is_dir():
				self.repo = pygit2.Repository(str(path))
			else:
				self.repo = pygit2.clone_repository(project.repo_url, str(path),
					bare=True)
			if revision is None or self.repo.get(revision) is None:
				self.repo.remotes.set_url('origin', project.repo_url)
				self.repo.remotes['origin'].fetch()
			if revision is None:
				self.revision = 'HEAD'
			elif self.repo.get(revision) is not None:
				self.revision = revision
			else:
				raise RuntimeError('No reivision')
		except pygit2.GitError as e:
			raise RuntimeError('Fetch problem') from e

	def revparse(self, rev):
		commit = self.repo.revparse_single(rev)
		return int.from_bytes(commit.id.raw[:4], 'big')

	def head(self):
		commit = self.repo.revparse_single(self.revision)
		return str(commit.id)[:7]

	def prev(self):
		try:
			commit = self.repo.revparse_single(self.revision + '^')
			return str(commit.id)[:7]
		except KeyError:
			return None

	def getTreeFiles(self, tree, prefix, recursive):
		for te in tree:
			filename = str(Path(prefix, te.name))
			if te.type == 'tree' and recursive:
				yield from self.getTreeFiles(self.repo[te.id], filename, recursive)
			else:
				File = namedtuple('File', ['id', 'path'])
				yield File(te.id, filename)

	def getFiles(self, revision, recursive=False):
		commit = self.repo.revparse_single(revision)
		yield from self.getTreeFiles(commit.tree, '', recursive)

	def getFile(self, hid):
		blob = self.repo.revparse_single(hid)
		if blob.type != 3:
			return KeyError(hid)
		return blob

	def getObjectByTreePath(self, tree, prefix, path):
		for te in tree:
			filename = str(Path(prefix, te.name))
			if path == filename:
				return RepositoryObjectWrapper(self.repo[te.id])
			if te.type == 'tree' and path.startswith(filename + '/'):
				return self.getObjectByTreePath(self.repo[te.id], filename, path)
		raise KeyError(prefix)

	def getObjectByPath(self, revision, path):
		commit = self.repo.revparse_single(revision)
		return self.getObjectByTreePath(commit.tree, '', path)
