from base.models import File, Issue


class ReportStorage:
	def __init__(self, project, repo=None):
		self.project = project
		self.repo = repo

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

		issues = [(i.file.path, i.line, i.position, i.text)
				for i in Issue.objects.filter(project=self.project)]
		newissues = list()
		for ni in report.issues():
			filename = filemap[ni.file]
			if (filename, ni.line, ni.position, ni.message) not in issues:
				issues.append((filename, ni.line, ni.position, ni.message))
				ii = Issue(project=self.project, file=files[filename],
					line=ni.line, position=ni.position, text=ni.message)
				newissues.append(ii)
		Issue.objects.bulk_create(newissues)
