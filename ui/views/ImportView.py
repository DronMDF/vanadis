from xml.etree import ElementTree
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from base.models import File, Issue, Project


@method_decorator(csrf_exempt, name='dispatch')
class ImportView(View):
	def post(self, request, **kwargs):
		projectname = kwargs['projectname']
		project = get_object_or_404(Project, name=projectname)

		it = ElementTree.parse(request)
		issues = []
		for f in it.findall('./file'):
			file = File.objects.create(project=project, path=f.findtext('./path'))
			for i in f.findall('./issue'):
				issues.append(Issue(project=project, file=file,
					line=int(i.findtext('./line')),
					position=int(i.findtext('./position', default=0)),
					text=i.findtext('./message'), code='null'))
		Issue.objects.bulk_create(issues)

		return HttpResponse()
