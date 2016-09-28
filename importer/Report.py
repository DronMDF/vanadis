import os
import re


class Issue:
	def __init__(self, filename, line, position, message, code):
		self.file = self.canonicalPath(filename)
		self.line = line
		self.position = position
		self.message = message
		self.code = code

	def canonicalPath(self, path):
		np = os.path.normpath(path)
		return np.lstrip('./')

	def __hash__(self):
		return hash((self.file, self.line, self.position, self.message, self.code))

	def __eq__(self, other):
		if self.line != other.line:
			return False
		if self.position != other.position:
			return False
		if self.file != other.file:
			return False
		if self.message != other.message:
			return False
		if self.code != other.code:
			return False
		return True


class IssueStream:
	def __init__(self, stream):
		self.stream = stream

	def __iter__(self):
		return self

	def __next__(self):
		for rl in self.stream:
			m1 = re.match(r'^(.*):(\d+):(\d+): (warning: .*)$', rl)
			if m1:
				return Issue(m1.group(1), int(m1.group(2)), int(m1.group(3)),
					m1.group(4), next(self.stream).rstrip())
			m2 = re.match((r'^\[(.*?):(\d+)\].*: '
				r'\((error|warning|performance|style)\) (.*)$'), rl)
			if m2:
				return Issue(m2.group(1), int(m2.group(2)), 0,
					m2.group(3) + ': ' + m2.group(4), '')
		raise StopIteration


class Report:
	def __init__(self, stream):
		issues = list(IssueStream(stream))
		filemap = self.generateFileMap((i.file for i in issues))
		self._files = set(filemap.values())
		self._issues = set()
		for i in issues:
			i.file = filemap[i.file]
			self._issues.add(i)

	def generateFileMap(self, files):
		fm = {}
		for f in sorted(set(files), key=len, reverse=True):
			ff = next((ff for ff in fm.keys() if ff.endswith('/' + f)), f)
			fm[f] = ff
		return fm

	def files(self):
		return iter(self._files)

	def issues(self):
		return iter(self._issues)
