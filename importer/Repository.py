from base64 import urlsafe_b64encode as b64encode
from pathlib import Path
import pygit2


class RepositoryObjectWrapper:
	def __init__(self, obj):
		self.id = obj.id
		self.obj = obj

	def is_dir(self):
		return self.obj.type == 2


class RepositoryId:
	def __init__(self, oid):
		self.oid = oid

	def base64(self):
		return b64encode(self.oid.raw[:6])


class RepositoryTreeObject:
	''' This is a tree object (blob or tree) '''
	def __init__(self, entry, prefix):
		self.entry = entry
		self.prefix = prefix

	def id(self):
		return RepositoryId(self.entry.id)

	def path(self):
		return str(Path(self.prefix, self.entry.name))

	def name(self):
		return self.entry.name


class Repository:
	def __init__(self, project):
		if project.repo_url is None:
			raise RuntimeError('No repository url')
		try:
			path = Path('/tmp/repos', project.name)
			if path.is_dir():
				self.repo = pygit2.Repository(str(path))
			else:
				self.repo = pygit2.clone_repository(project.repo_url, str(path),
					bare=True)
			self.repo.remotes.set_url('origin', project.repo_url)
			self.repo.remotes['origin'].fetch()
		except pygit2.GitError as e:
			raise RuntimeError('Fetch problem') from e

	def revparse(self, rev):
		commit = self.repo.revparse_single(rev)
		return int.from_bytes(commit.id.raw[:4], 'big')

	def head(self):
		commit = self.repo.revparse_single('HEAD')
		return str(commit.id)[:7]

	def prev(self):
		try:
			commit = self.repo.revparse_single('HEAD^')
			return str(commit.id)[:7]
		except KeyError:
			return None

	def getTreeFiles(self, tree, prefix, recursive):
		for te in tree:
			filename = str(Path(prefix, te.name))
			yield RepositoryTreeObject(te, prefix)
			if te.type == 'tree' and recursive:
				yield from self.getTreeFiles(self.repo[te.id], filename, recursive)

	def tree(self, revision, recursive=False):
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
