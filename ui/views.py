from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from base.models import Project


def index(request):
	projects = Project.objects.all()
	context = {'projects': projects}
	return render(request, 'ui/index.html', context)


def project(request, id):
	project = get_object_or_404(Project, id=id)
	context = {'project': project, 'revisions': [], 'branches': [], 'files': []}
	return render(request, 'ui/project.html', context)


class CreateProjectView(View):
	def createProject(self, name):
		Project.objects.create(name=name)

	def post(self, request, *args, **kwargs):
		self.createProject(request.POST['name'])
		return redirect('/ui')

	def get(self, request, *args, **kwargs):
		self.createProject(request.GET['name'])
		return redirect('/ui')
