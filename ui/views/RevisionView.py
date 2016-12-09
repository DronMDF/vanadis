from django.shortcuts import get_object_or_404
from base.models import Project
from ui import DirectoryObject
from ui.views import RepositoryBaseView


class RevisionView(RepositoryBaseView):
	template_name = 'revision.xml'
	content_type = 'text/xml'

	def getObjects(self, repo, revision, view):
		if view == 'recursive':
			return repo.tree(revision)
		else:
			return DirectoryObject(repo.tree(revision))

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
		view = self.request.GET.get('view', 'onelevel')
		files = self.getObjects(repo, revision, view)
		context['files'] = [{'id': f.id().base64(), 'path': f.path(),
			'name': f.path(), 'issue_count': 0} for f in files]
		return context
