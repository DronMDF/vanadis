from django.http import Http404
from django.views.generic import TemplateView
from importer.Repository import Repository


class RepositoryBaseView(TemplateView):
	def getRepository(self, project, revision=None):
		try:
			return Repository(project, revision)
		except RuntimeError:
			raise Http404('Cannot open repository')
