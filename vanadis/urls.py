from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = [
	url(r'^$', RedirectView.as_view(url='ui/', permanent=False), name='index'),
	url(r'^ui/', include('webui.urls')),
	url(r'^admin/', admin.site.urls),
]
