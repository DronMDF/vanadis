from pathlib import Path


class DirectoryObject:
	''' One level objects filter '''
	def __init__(self, tree, directory=''):
		self.tree = iter(tree)
		self.directory = directory

	def __iter__(self):
		return self

	def __next__(self):
		for o in self.tree:
			if o.path() == str(Path(self.directory, o.name())):
				return o
		raise StopIteration()
