from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from importer.views import entry

urlpatterns = [
	url(r'^$', RedirectView.as_view(url='/ui', permanent=False), name='index'),
	url(r'^ui/', include('ui.urls')),
	url(r'^import/', entry),
	url(r'^admin/', admin.site.urls),
]
