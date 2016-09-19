from base.models import File, Issue


class ReportStorage:
	def __init__(self, project):
		self.project = project

	def issueInList(self, issue, issues):
		return (issue.file, issue.line, issue.position, issue.text, issue.code) in [
			(i.file, i.line, i.position, i.text, i.code) for i in issues]

	def pathMatch(self, p, ef):
		for ee in ef:
			if ee == p or ee.endswith('/' + p) or p.endswith('/' + ee):
				return p, ee
		return p, None

	def pathMatchMap(self, rf, ef):
		for rr in rf:
			yield self.pathMatch(rr, ef)

	def updateFiles(self, reportfiles):
		filenames = {f.path for f in File.objects.filter(project=self.project)}
		filemap = dict(self.pathMatchMap(reportfiles, filenames))

		for f, e in filemap.items():
			if e is not None and f.endswith('/' + e):
				# This is very rare case, not need to optimize
				File.objects.filter(project=self.project, path=e).update(path=f)

		newfiles = (f for f, e in filemap.items() if e is None)
		File.objects.bulk_create([File(project=self.project, path=f) for f in newfiles])

	def importReport(self, report):
		self.updateFiles(report.files())

		# generate new file list
		files = {f.path: f for f in File.objects.filter(project=self.project)}
		filemap = dict(self.pathMatchMap(report.files(), files.keys()))

		issues = list(Issue.objects.filter(project=self.project))
		newissues = list()
		for ni in report.issues():
			if filemap[ni.file] is not None:
				filename = filemap[ni.file]
			else:
				filename = ni.file
			ii = Issue(project=self.project, file=files[filename], line=ni.line,
				position=ni.position, text=ni.message, code=ni.code)
			if not self.issueInList(ii, issues) and not self.issueInList(ii, newissues):
				newissues.append(ii)
		Issue.objects.bulk_create(newissues)
