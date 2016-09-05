import re
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, render, get_object_or_404
from base.models import Issue, Project
from .issue import generateIssues


@require_POST
@csrf_protect
def entry(request):
	project = get_object_or_404(Project, name=request.POST['project'])
	Issue.objects.bulk_create(generateIssues(request.FILES['log'], project))
	return redirect('/ui/project/%s/' % project.name)
