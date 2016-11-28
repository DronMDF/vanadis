import binascii
from xml.etree import ElementTree
from django.http.response import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from base.models import File, Issue, Object, Project
from . import RepositoryBaseView


@method_decorator(csrf_exempt, name='dispatch')
class ImportView(RepositoryBaseView):
	def getRevision(self, project, revision):
		try:
			repository = self.getRepository(project)
			return repository.revparse(revision)
		except:
			raise Http404("Revision was not found")

	def post(self, request, **kwargs):
		projectname = kwargs['projectname']
		project = get_object_or_404(Project, name=projectname)

		self.getRevision(project, kwargs['revision'])
		it = ElementTree.parse(request)
		issues = []
		for f in it.findall('./file'):
			file = File.objects.create(project=project, path=f.findtext('./path'))
			oid = int.from_bytes(binascii.unhexlify(f.findtext('./oid')), 'big')
			obj = Object.objects.create(project=project, oid=oid, issues_count=0)
			for i in f.findall('./issue'):
				issues.append(Issue(project=project, file=file, object=obj,
					line=int(i.findtext('./line')),
					position=int(i.findtext('./position', default=0)),
					text=i.findtext('./message')))
		Issue.objects.bulk_create(issues)

		return HttpResponse()
