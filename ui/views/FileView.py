from itertools import groupby
from django.shortcuts import get_object_or_404
from base.models import Issue, Project
from ui import DirectoryObject, TreeObject
from ui.views import RepositoryBaseView


class FileView(RepositoryBaseView):
	content_type = 'text/xml'

	def get_template_names(self):
		projectname = self.kwargs['projectname']
		project = get_object_or_404(Project, name=projectname)
		revision = self.kwargs['revision']
		filename = self.kwargs['filename']
		repo = self.getRepository(project)
		obj = TreeObject(repo.tree(revision), filename)
		return 'revision.xml' if obj.is_dir() else 'file.xml'

	def sortedLineIssue(self, issues):
		return [{
			'position': i.position,
			'text': i.text
		} for i in sorted(list(issues), key=lambda i: i.position, reverse=True)]

	def generateSourceLine(self, line, issues):
		return {
			'lineno': line,
			'code': '',
			'issues': self.sortedLineIssue(issues)
		}

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		projectname = kwargs['projectname']
		project = get_object_or_404(Project, name=projectname)
		revision = kwargs['revision']
		filename = kwargs['filename']
		repo = self.getRepository(project)
		obj = TreeObject(repo.tree(revision), filename)
		if obj.is_dir():
			context['projectname'] = projectname
			context['revision'] = repo.head()
			previous = repo.prev()
			if previous is not None:
				context['previous'] = previous
			context['base_path'] = filename
			context['files'] = [{'id': f.id().base64(), 'path': f.path(),
				'name': f.name(), 'issue_count': 0} for f in DirectoryObject(
					repo.tree(revision), filename)]
		else:
			issues = Issue.objects.filter(project=project,
				file__path=filename).order_by('line')
			lines = groupby(issues, lambda i: i.line)
			context['projectname'] = projectname
			context['path'] = filename
			context['lines'] = [self.generateSourceLine(l, list(ii)) for l, ii in lines]
		return context
