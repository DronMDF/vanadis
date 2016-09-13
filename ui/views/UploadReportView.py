from django.forms import Form, FileField
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from importer.issue import uploadReport


class UpdateReportForm(Form):
	report = FileField()


class UploadReportView(FormView):
	template_name = 'ui/upload_report.html'
	form_class = UpdateReportForm

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data()
		context_data['projectname'] = kwargs['projectname']
		return context_data

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
			projectname = kwargs['projectname']
			uploadReport(projectname, request.FILES['report'])
			return redirect('/ui/project/%s' % projectname)
		else:
			return self.form_invalid(form)
