from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from base.models import File, Issue, Project
from ui.views import RepositoryBaseView


class ProjectView(RepositoryBaseView):
	template_name = 'project.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		projectname = kwargs['projectname']
		project = get_object_or_404(Project, name=projectname)
		files = File.objects.filter(project=project).order_by('path')
		files_info = [{
			'name': f.path,
			'issue_count': Issue.objects.filter(file=f).count()
		} for f in files]
		context['project'] = project
		context['files'] = files_info
		return context

	def get(self, request, *args, **kwargs):
		projectname = kwargs['projectname']
		project = get_object_or_404(Project, name=projectname)
		try:
			repo = self.getRepository(project)
			return redirect('/%s/%s' % (project.name, repo.head()))
		except Http404:
			pass
		return super().get(request, *args, **kwargs)
