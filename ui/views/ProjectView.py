from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from base.models import Issue, Project


class ProjectView(TemplateView):
	template_name = 'ui/project.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		projectname = kwargs['name']
		project = get_object_or_404(Project, name=projectname)
		files = [{
			'name': f,
			'issue_count': len(Issue.objects.filter(project=project, file=f))
		} for f in sorted(set((i.file for i in Issue.objects.filter(project=project))))]
		context['project'] = project
		context['files'] = files
		return context
