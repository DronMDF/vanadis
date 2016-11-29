import binascii


class FakeOid:
	def __init__(self, oid):
		self.raw = binascii.unhexlify(oid)


class FakeFile:
	def __init__(self, path, oid='0123456789012'):
		self.path = path
		self.oid = FakeOid(oid)


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
