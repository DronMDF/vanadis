
class FakeFile:
	def __init__(self, path):
		self.path = path
		self.oid = '01234567'


class FakeRepository:
	def __init__(self, *revs, files=list()):
		self.revs = revs
		self.files = files

	def revparse(self, revision):
		return revision

	def head(self):
		return self.revs[-1]

	def prev(self):
		return self.revs[-2]

	def getFiles(self, revision):
		del revision
		return self.files
