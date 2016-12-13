from pathlib import Path
import pygit2
from ui import RepositoryTree


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

	def tree(self, revision):
		commit = self.repo.revparse_single(revision)
		return RepositoryTree(commit.tree, self.repo)

	def getFile(self, hid):
		blob = self.repo.revparse_single(hid)
		if blob.type != 3:
			return KeyError(hid)
		return blob
