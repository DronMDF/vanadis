import re
from base.models import Issue


def generateIssues(log, project):
	for ll in log:
		mo = re.match('^(.*):(\d+):(\d+): warning: (.*)$', ll.decode('utf8'))
		if mo:
			yield Issue(
				project=project, file=mo.group(1), line=mo.group(2),
				position=mo.group(3), text=mo.group(4))
