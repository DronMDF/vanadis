from django.conf.urls import url
from .views import (FileView, ImportView, MainView, NewProjectView, ProjectSettingView, ProjectView,
	RevisionView)

urlpatterns = [
	url(r'^$', MainView.as_view(), name='index'),
	url(r'^newproject$', NewProjectView.as_view()),
	url(r'^(?P<projectname>[\w-]+)$', ProjectView.as_view()),
	url(r'^(?P<projectname>[\w-]+)/import/(?P<revision>[0-9a-fA-F]{7,})', ImportView.as_view()),
	url(r'^(?P<projectname>[\w-]+)/settings$', ProjectSettingView.as_view()),
	url(r'^(?P<projectname>[\w-]+)/(?P<revision>[0-9a-fA-F]{7})$', RevisionView.as_view()),
	url(r'^(?P<projectname>[\w-]+)/(?P<revision>[0-9a-fA-F]{7})/(?P<filename>.*)$',
		FileView.as_view()),
]
