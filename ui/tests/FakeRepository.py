class FakeRepository:
	def __init__(self, *revs):
		self.revs = revs

	def head(self):
		return self.revs[-1]

	def prev(self):
		return self.revs[-2]
