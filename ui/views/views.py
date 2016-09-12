import re
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from base.models import Project


# TODO: This is old style functional view. Need to migrate to Class Based Form View
@require_POST
@csrf_protect
def createProject(request):
	name = request.POST['name']
	if not re.match('^[a-zA-Z]{1}[\w-]{1,98}[a-zA-Z0-9]{1}$', name):
		return HttpResponseBadRequest()
	Project.objects.create(name=name)
	return redirect('/ui')
