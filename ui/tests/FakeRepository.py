import binascii


class FakeOid:
	def __init__(self, oid):
		self.raw = binascii.unhexlify(oid)


class FakeFile:
	def __init__(self, path, oid='0123456789012'):
		self.path = path
		self.oid = FakeOid(oid)


class FakeRepository:
	def __init__(self, commits=None, files=None):
		self.revs = commits if commits is not None else []
		self.files = files if files is not None else []

	def revparse(self, revision):
		for r in self.revs:
			if revision in r:
				return revision
		raise KeyError('No revision')

	def head(self):
		return self.revs[-1]

	def prev(self):
		return self.revs[-2]

	def getFiles(self, _):
		return self.files
