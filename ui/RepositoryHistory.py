from binascii import hexlify
from ui import RepositoryTreeObject


class Zero:
	raw = b'\0' * 24

	def __str__(self):
		return hexlify(self.raw).decode('ascii')


class Commit:
	id = Zero()


class RepositoryHistory:
	def __init__(self, commit):
		self.head = commit

	def __iter__(self):
		c = self.head
		while c is not None:
			yield RepositoryTreeObject(c, '')
			c = next(iter(c.parents), None)
		while True:
			yield RepositoryTreeObject(Commit(), '')
