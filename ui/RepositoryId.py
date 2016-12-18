from base64 import urlsafe_b64encode as b64encode


class RepositoryId:
	def __init__(self, oid):
		self.oid = oid

	def __str__(self):
		return str(self.oid)[:7]

	def base64(self):
		return b64encode(self.oid.raw[:6])

	def int(self):
		return int.from_bytes(self.oid.raw[:7], 'big')
