from django.views.decorators.csrf import csrf_protect
from django.http.response import HttpResponse


@csrf_protect
def entry(request):
	return HttpResponse()
