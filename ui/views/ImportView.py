from binascii import hexlify
from base64 import urlsafe_b64decode as b64decode
from xml.etree import ElementTree
from django.http.response import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from base.models import Issue, Object, Project
from . import RepositoryBaseView


class ExistIssue:
	def __init__(self, issue):
		self.issue = issue

	def __eq__(self, o):
		return all((self.issue.object == o.issue.object,
			self.issue.line == o.issue.line,
			self.issue.position == o.issue.position,
			self.issue.text == o.issue.text))

	def __hash__(self):
		return hash((self.issue.object, self.issue.line, self.issue.position,
			self.issue.text))


class NewIssue:
	def __init__(self, **kwargs):
		self.issue = Issue(**kwargs)

	def __eq__(self, o):
		return all((self.issue.object == o.issue.object,
			self.issue.line == o.issue.line,
			self.issue.position == o.issue.position,
			self.issue.text == o.issue.text))

	def __hash__(self):
		return hash((self.issue.object, self.issue.line, self.issue.position,
			self.issue.text))

	def asIssue(self):
		return self.issue


@method_decorator(csrf_exempt, name='dispatch')
class ImportView(RepositoryBaseView):
	def getRevision(self, repo, revision):
		try:
			return repo.revparse(revision)
		except:
			raise Http404("Revision not found")

	def getFileId(self, repo, xid):
		if not isinstance(xid, str):
			raise Http404("File not found")
		fileid = b64decode(xid)
		file = repo.getFile(hexlify(fileid).decode('ascii'))
		return file.id().int()

	def post(self, request, **kwargs):
		projectname = kwargs['projectname']
		project = get_object_or_404(Project, name=projectname)
		repo = self.getRepository(project)
		self.getRevision(repo, kwargs['revision'])
		it = ElementTree.parse(request)
		issues = set()
		for f in it.findall('./file'):
			oid = self.getFileId(repo, f.findtext('./id'))
			try:
				obj = Object.objects.get(project=project, oid=oid)
				issues.update((ExistIssue(i)
					for i in Issue.objects.filter(object=obj)))
			except Object.DoesNotExist:
				obj = Object.objects.create(project=project, oid=oid,
					issues_count=0)
			for i in f.findall('./issue'):
				issues.add(NewIssue(project=project, object=obj,
					line=int(i.findtext('./line')),
					position=int(i.findtext('./position', default=0)),
					text=i.findtext('./message')))
		Issue.objects.bulk_create((i.asIssue() for i in issues if isinstance(i, NewIssue)))
		return HttpResponse()
