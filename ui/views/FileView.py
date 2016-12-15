from django.shortcuts import get_object_or_404
from base.models import Issue, Project
from ui import DirectoryObject, TreeObjectsWithPathname
from ui.views import RepositoryBaseView


class FileView(RepositoryBaseView):
	content_type = 'text/xml'

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.obj = None

	def get_template_names(self):
		return 'revision.xml' if self.obj.is_dir() else 'file.xml'

	def generateLines(self, content, issues):
		for lineno, line in enumerate(content):
			yield {
				'lineno': lineno + 1,
				'code': line,
				'issues': [{
					'position': i.position,
					'text': i.text
				} for i in issues if i.line == lineno + 1]
			}

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		projectname = kwargs['projectname']
		project = get_object_or_404(Project, name=projectname)
		revision = kwargs['revision']
		filename = kwargs['filename']
		repo = self.getRepository(project)
		self.obj = next(iter(TreeObjectsWithPathname(repo.tree(revision), filename)))

		context['projectname'] = projectname
		context['revision'] = repo.head()
		previous = repo.prev()
		if previous is not None:
			context['previous'] = previous
		context['path'] = filename

		if self.obj.is_dir():
			context['files'] = [{'id': f.id().base64(), 'path': f.path(),
				'name': f.name(), 'issue_count': 0} for f in DirectoryObject(
					repo.tree(revision), filename)]
		else:
			content = self.obj.content().split('\n')
			issues = list(Issue.objects.filter(project=project,
				object__oid=self.obj.id().int()))
			context['lines'] = list(self.generateLines(content, issues))
		return context
