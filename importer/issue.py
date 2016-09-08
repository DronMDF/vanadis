import re
from base.models import Issue


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
