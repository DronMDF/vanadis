import re
from django.forms import ModelForm, ValidationError
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from base.models import Project


class NewProjectForm(ModelForm):
	class Meta:
		model = Project
		fields = ['name']

	def clean(self):
		cleaned_data = super().clean()
		name = cleaned_data.get('name', '')
		if not re.match('^[a-zA-Z]{1}[\w-]{1,98}[a-zA-Z0-9]{1}$', name):
			raise ValidationError('Invalid value')
		return cleaned_data


class NewProjectView(FormView):
	template_name = 'ui/new_project.html'
	form_class = NewProjectForm

	def form_valid(self, form):
		project = form.save()
		return redirect('/ui/project/%s' % project.name)
