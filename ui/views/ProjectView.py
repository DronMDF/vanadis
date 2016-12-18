from django.shortcuts import get_object_or_404, redirect
from base.models import Project
from ui.views import RepositoryBaseView


class ProjectView(RepositoryBaseView):
	def get(self, request, *args, **kwargs):
		projectname = kwargs['projectname']
		project = get_object_or_404(Project, name=projectname)
		repo = self.getRepository(project)
		log = iter(repo.log())
		return redirect('/%s/%s' % (project.name, str(next(log).id())))
