from . import RepositoryBaseView


class IssuesView(RepositoryBaseView):
	template_name = 'issues.xml'
	content_type = 'text/xml'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['issues'] = []
		return context
