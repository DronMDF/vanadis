from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from base.models import Project
from importer.Repository import Repository


class RevisionView(TemplateView):
	template_name = 'project_revision.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		projectname = kwargs['projectname']
		project = get_object_or_404(Project, name=projectname)
		try:
			repo = Repository(project)
		except RuntimeError:
			return Http404('Reposytory does not exists')
		context['project'] = project
		context['prev'] = repo.prev()
		context['head'] = repo.head()
		context['files'] = []
		return context
