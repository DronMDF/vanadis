from base64 import urlsafe_b64encode as b64encode
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
		repo = self.getRepository(project, revision)
		context['revision'] = repo.head()
		previous = repo.prev()
		if previous is not None:
			context['previous'] = previous
		recursive = (kwargs.get('view', 'onelevel') == 'recursive')
		context['files'] = [{'id': b64encode(f.id.raw[:6]), 'path': f.path,
			'issue_count': 0} for f in repo.getFiles(revision, recursive)]
		return context
