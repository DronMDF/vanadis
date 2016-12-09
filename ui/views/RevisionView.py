from django.shortcuts import get_object_or_404
from base.models import Project
from ui.views import RepositoryBaseView


class RevisionView(RepositoryBaseView):
	template_name = 'revision.xml'
	content_type = 'text/xml'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		projectname = kwargs['projectname']
		project = get_object_or_404(Project, name=projectname)
		context['project'] = project

		revision = kwargs['revision']
		repo = self.getRepository(project)
		context['revision'] = repo.head()
		previous = repo.prev()
		if previous is not None:
			context['previous'] = previous
		recursive = (self.request.GET.get('view', 'onelevel') == 'recursive')
		context['files'] = [{'id': f.id().base64(), 'path': f.path(),
			'name': f.path() if recursive else f.name(),
			'issue_count': 0} for f in repo.tree(revision, recursive)]
		return context
