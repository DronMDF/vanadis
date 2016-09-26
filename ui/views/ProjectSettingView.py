from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from base.models import Project


class ProjectSettingView(UpdateView):
	fields = []
	model = Project
	template_name = 'ui/project_settings.html'

	def get_object(self):
		name = self.kwargs['projectname']
		return get_object_or_404(Project, name=name)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['projectname'] = self.object.name
		return context

	def get_success_url(self):
		return '/ui/project/%s' % self.object.name
