from pathlib import Path
import pygit2
from ui import RepositoryTree


class Repository:
	def __init__(self, project):
		self.name = project.name
		self.url = project.repo_url

	def openRepository(self):
		path = str(Path('/var/tmp/vanadis', self.name))
		try:
			repo = pygit2.Repository(path)
		except KeyError:
			repo = pygit2.init_repository(path, bare=True)

		if 'origin' in (r.name for r in repo.remotes):
			repo.remotes.delete('origin')

		try:
			repo.remotes.create('origin', self.url)
			repo.remotes['origin'].fetch()
		except pygit2.GitError as e:
			raise RuntimeError('Problem with fetch git repository') from e

		return repo

	def revparse_single(self, revision):
		return self.openRepository().revparse_single(revision)

	def revparse(self, rev):
		commit = self.revparse_single(rev)
		return int.from_bytes(commit.id.raw[:4], 'big')

	def head(self):
		commit = self.revparse_single('HEAD')
		return str(commit.id)[:7]

	def prev(self):
		try:
			commit = self.revparse_single('HEAD^')
			return str(commit.id)[:7]
		except KeyError:
			return None

	def tree(self, revision):
		repo = self.openRepository()
		commit = repo.revparse_single(revision)
		return RepositoryTree(commit.tree, repo)

	def getFile(self, hid):
		blob = self.revparse_single(hid)
		if blob.type != 3:
			return KeyError(hid)
		return blob
