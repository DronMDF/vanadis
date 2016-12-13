from django.http import Http404
from django.views.generic import TemplateView
from ui import Repository


class RepositoryBaseView(TemplateView):
	def getRepository(self, project):
		try:
			return Repository(project)
		except RuntimeError:
			raise Http404('Cannot open repository')
