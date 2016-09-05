import re
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET, require_POST
from base.models import Project


@require_GET
def index(request):
	projects = Project.objects.all()
	context = {'projects': projects}
	return render(request, 'ui/index.html', context)


@require_GET
def project(request, name):
	project = get_object_or_404(Project, name=name)
	context = {'project': project, 'revisions': [], 'branches': [], 'files': []}
	return render(request, 'ui/project.html', context)


@require_POST
@csrf_protect
def createProject(request):
	name = request.POST['name']
	if not re.match('^[a-zA-Z]{1}[\w-]{1,98}[a-zA-Z0-9]{1}$', name):
		return HttpResponseBadRequest()
	Project.objects.create(name=name)
	return redirect('/ui')
