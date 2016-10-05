from pathlib import Path
import pygit2


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

	def head(self):
		commit = self.repo.revparse_single(self.revision)
		return str(commit.id)[:7]

	def prev(self):
		commit = self.repo.revparse_single(self.revision + '^')
		return str(commit.id)[:7]
