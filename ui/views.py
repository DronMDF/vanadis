from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from base.models import Project


def index(request):
	return render(request, 'ui/index.html', {})


class CreateProjectView(View):
	def createProject(self, name):
		Project.objects.create(name=name)

	def post(self, request, *args, **kwargs):
		self.createProject(request.POST['name'])
		return redirect('/ui')

	def get(self, request, *args, **kwargs):
		self.createProject(request.GET['name'])
		return redirect('/ui')
