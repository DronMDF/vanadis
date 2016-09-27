from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = [
	url(r'', include('ui.urls'))
]
