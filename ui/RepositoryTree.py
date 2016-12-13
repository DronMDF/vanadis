from pathlib import Path
from . import RepositoryTreeObject


class RepositoryTree:
	def __init__(self, tree, repo):
		self.tree = tree
		self.repo = repo

	def getTreeFiles(self, tree, prefix):
		for te in tree:
			filename = str(Path(prefix, te.name))
			yield RepositoryTreeObject(te, prefix, self.repo)
			if te.type == 'tree':
				yield from self.getTreeFiles(self.repo[te.id], filename)

	def __iter__(self):
		yield from self.getTreeFiles(self.tree, '')
