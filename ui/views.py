from django.http import HttpResponse
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
def project(request, id):
	project = get_object_or_404(Project, id=id)
	context = {'project': project, 'revisions': [], 'branches': [], 'files': []}
	return render(request, 'ui/project.html', context)


@require_POST
@csrf_protect
def createProject(request):
	Project.objects.create(name=request.POST['name'])
	return redirect('/ui')
