class TreeObject:
	def __init__(self, tree, path):
		self.tree = tree
		self.path = path

	def id(self):
		for o in self.tree:
			if o.path() == self.path:
				return o.id()
		raise KeyError(self.path)

	def is_dir(self):
		for o in self.tree:
			if o.path() == self.path:
				return o.is_dir()
		raise KeyError(self.path)

	def content(self):
		for o in self.tree:
			if o.path() == self.path:
				return o.content()
		raise KeyError(self.path)
