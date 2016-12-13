from pathlib import Path
from ui import RepositoryId


class RepositoryTreeObject:
	''' This is a tree object (blob or tree) '''
	def __init__(self, entry, prefix, repo=None):
		self.entry = entry
		self.prefix = prefix
		self.repo = repo

	def id(self):
		return RepositoryId(self.entry.id)

	def path(self):
		return str(Path(self.prefix, self.entry.name))

	def name(self):
		return self.entry.name

	def is_dir(self):
		return self.entry.type == 'tree'

	def content(self):
		return self.repo[self.entry.id].data.decode('utf8')
