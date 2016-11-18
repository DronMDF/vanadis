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
		valid_re = [r'^[a-zA-Z]+', r'[a-zA-Z0-9]+$', r'^[\w-]+$']
		if not all((re.search(e, name) for e in valid_re)):
			raise ValidationError('Invalid value')
		return cleaned_data


class NewProjectView(FormView):		# pylint: disable=too-many-ancestors
	template_name = 'new_project.html'
	form_class = NewProjectForm

	def form_valid(self, form):
		project = form.save()
		return redirect('/%s' % project.name)
