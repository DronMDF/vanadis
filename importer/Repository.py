from pathlib import Path
import pygit2


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

	def head(self):
		ref = self.repo.lookup_reference('HEAD')
		return str(ref.peel().id)[:7]
