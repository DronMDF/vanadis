import os
import re
from django.shortcuts import get_object_or_404
from base.models import Issue, Project


class FileRepr:
	def __init__(self, path):
		self.path = ''
		self.update(path)

	def update(self, path):
		np = os.path.normpath(path)
		if np.startswith('../'):
			np = np.lstrip('./')
		if len(self.path) < len(np):
			self.path = np


class IssueRepr:
	def __init__(self, project, file, line, position, message, code):
		self.project = project
		self.file = file
		self.line = line
		self.position = position
		self.message = message.rstrip()
		self.code = code.rstrip()

	def __hash__(self):
		return hash((self.file, self.line, self.position, self.message, self.code))

	def __eq__(self, other):
		sd = (self.file, self.line, self.position, self.message, self.code)
		od = (other.file, other.line, other.position, other.message, other.code)
		return sd == od

	def asModel(self):
		return Issue(project=self.project, file=self.file.path, line=self.line,
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


def generateIssueRepr(log, project):
	files = dict()
	for il in splitReportToIssueChain(log):
		if len(il) < 1:
			continue
		mo = re.match('^(.*):(\d+):(\d+): warning: (.*)$', il[0].decode('utf8'))
		if mo and len(il) >= 2:
			filename = mo.group(1)
			filekey = filename.split('/')[-1]
			if filekey not in files:
				files[filekey] = FileRepr(filename)
			else:
				files[filekey].update(filename)
			yield IssueRepr(project, files[filekey], mo.group(2), mo.group(3),
				mo.group(4), il[1])


def generateIssues(log, project):
	for ir in set(generateIssueRepr(log, project)):
		yield ir.asModel()


def uploadReport(projectname, report):
	project = get_object_or_404(Project, name=projectname)
	Issue.objects.bulk_create(generateIssues(report, project))
