from itertools import groupby
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from base.models import Issue, Project


class FileView(TemplateView):
	template_name = 'ui/file.html'

	def sortedLineIssue(self, issues):
		return [{
			'position': i.position,
			'text': i.text
		} for i in sorted(list(issues), key=lambda i: i.position, reverse=True)]

	def generateSourceLine(self, line, issues):
		return {
			'line': line,
			'code': issues[0].code,
			'issues': self.sortedLineIssue(issues)
		}

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		projectname = kwargs['projectname']
		filename = kwargs['filename']
		project = get_object_or_404(Project, name=projectname)
		issues = Issue.objects.filter(project=project, file=filename).order_by('line')
		lines = groupby(issues, lambda i: i.line)
		context['project'] = project
		context['filename'] = filename
		context['sourcecode'] = [self.generateSourceLine(l, list(ii)) for l, ii in lines]
		return context
