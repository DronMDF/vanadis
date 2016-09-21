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
		sd = (self.file, self.line, self.position, self.message, self.code)
		od = (other.file, other.line, other.position, other.message, other.code)
		return sd == od


class Report:
	def __init__(self, report_text):
		self.report = set(self.generateIssues(report_text))

	def splitReportToIssueChain(self, log):
		issue_chain = []
		for ll in log.split('\n'):
			if re.match('^.*:\d+:\d+: warning: .*$', ll):
				if issue_chain:
					yield issue_chain
				issue_chain = []
			issue_chain.append(ll)
		yield issue_chain

	def generateIssues(self, log):
		files = dict()
		for il in self.splitReportToIssueChain(log):
			if len(il) < 1:
				continue
			mo = re.match('^(.*):(\d+):(\d+): warning: (.*)$', il[0])
			if mo and len(il) >= 2:
				filename = mo.group(1)
				yield Issue(mo.group(1), int(mo.group(2)), int(mo.group(3)),
					mo.group(4), il[1])

	def files(self):
		files = set()
		for i in self.report:
			if i.file not in files:
				files.add(i.file)
				yield i.file

	def issues(self):
		for i in self.report:
			yield i