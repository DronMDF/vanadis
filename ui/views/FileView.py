from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from base.models import Issue, Project


class FileView(TemplateView):
	template_name = 'ui/file.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		projectname = kwargs['projectname']
		filename = kwargs['filename']
		project = get_object_or_404(Project, name=projectname)
		context['project'] = project
		context['filename'] = filename
		context['issues'] = Issue.objects.filter(project=project,
				file=filename).order_by('line')
		return context
