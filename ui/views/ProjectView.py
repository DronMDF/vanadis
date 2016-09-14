from itertools import groupby
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from base.models import Issue, Project


class ProjectView(TemplateView):
	template_name = 'ui/project.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		projectname = kwargs['name']
		project = get_object_or_404(Project, name=projectname)
		issues = Issue.objects.filter(project=project).order_by('file')
		issues_by_file = groupby(issues, lambda i: i.file)
		files = [{'name': f, 'issue_count': len(list(ii))} for f, ii in issues_by_file]
		context['project'] = project
		context['files'] = files
		return context
