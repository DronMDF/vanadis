from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from base.models import Project


def index(request):
	return render(request, 'ui/index.html', {})


class CreateProjectView(View):
	def post(self, request, *args, **kwargs):
		Project.objects.create(name=request.POST['name'])
		return HttpResponse()
