from django.views.generic import TemplateView
from base.models import Issue, Project


class MainView(TemplateView, ):
	template_name = 'index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		projects = [{
			'name': p.name,
			'id': p.id,
			'issue_count': len(Issue.objects.filter(project=p.id))
		} for p in Project.objects.all()]
		context['projects'] = projects
		return context
