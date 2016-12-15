class TreeObjectsWithPathname:
	''' Collection of tree objects with specific path.
		In typical case size of this collection less or equal 1 '''
	def __init__(self, tree, path):
		self.tree = tree
		self.path = path

	def __iter__(self):
		for o in self.tree:
			if o.path() == self.path:
				yield o
