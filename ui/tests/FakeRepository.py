import binascii


class FakeOid:
	def __init__(self, oid):
		self.raw = binascii.unhexlify(oid)

	def __str__(self):
		return binascii.hexlify(self.raw).decode('ascii')


class FakeFile:
	def __init__(self, path, oid='0123456789012'):
		self.path = path
		self.id = FakeOid(oid)


class FakeRepository:
	def __init__(self, commits=None, files=None):
		self.revs = commits if commits is not None else []
		self.files = files if files is not None else []

	def revparse(self, revision):
		for r in self.revs:
			if r.startswith(revision):
				return revision
		raise KeyError(revision)

	def getFile(self, hid):
		for f in self.files:
			if str(f.id).startswith(hid):
				return f
		raise KeyError(hid)

	def head(self):
		return self.revs[-1]

	def prev(self):
		return self.revs[-2]

	def getFiles(self, _):
		return self.files
