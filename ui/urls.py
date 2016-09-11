from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^project$', views.createProject),
	url(r'^project/(?P<name>[\w-]+)/$', views.project),
	url(r'^project/(?P<projectname>[\w-]+)/(?P<filename>.*)$', views.file),
]
