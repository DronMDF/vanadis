from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View


@method_decorator(csrf_exempt, name='dispatch')
class ImportView(View):
	def post(self, request):
		for l in request:
			open('request.xml', 'w').write(l.decode('utf8'))
		return HttpResponse()
