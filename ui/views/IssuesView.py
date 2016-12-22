from django.shortcuts import get_object_or_404
from base.models import Project
from . import RepositoryBaseView


class IssuesView(RepositoryBaseView):
	template_name = 'issues.xml'
	content_type = 'text/xml'

	def get_context_data(self, **kwargs):
		projectname = kwargs['projectname']
		get_object_or_404(Project, name=projectname)
		context = super().get_context_data(**kwargs)
		context['issues'] = []
		return context
