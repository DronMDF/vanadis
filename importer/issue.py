import re
from base.models import Issue


class IssueRepr:
	def __init__(self, project, file, line, position, message, code):
		self.project = project
		self.file = file
		self.line = line
		self.position = position
		self.message = message
		self.code = code

	def __eq__(self, other):
		sd = (self.file.split('/')[-1], self.line, self.position, self.message, self.code)
		od = (other.file.split('/')[-1], other.line, other.position, other.message,
			other.code)
		return sd == od

	def asModel(self):
		return Issue(project=self.project, file=self.file, line=self.line,
			position=self.position, text=self.message, code=self.code)


def splitReportToIssueChain(log):
	issue_chain = []
	for ll in log:
		if re.match('^.*:\d+:\d+: warning: .*$', ll.decode('utf8')):
			if issue_chain:
				yield issue_chain
			issue_chain = []
		issue_chain.append(ll)
	yield issue_chain


def generateIssues(log, project):
	for il in splitReportToIssueChain(log):
		if len(il) < 1:
			continue
		mo = re.match('^(.*):(\d+):(\d+): warning: (.*)$', il[0].decode('utf8'))
		if mo and len(il) >= 2:
			yield Issue(
				project=project, file=mo.group(1), line=mo.group(2),
				position=mo.group(3), text=mo.group(4), code=il[1])
