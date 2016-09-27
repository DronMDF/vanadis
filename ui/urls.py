from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^$', MainView.as_view(), name='index'),
	url(r'^newproject$', NewProjectView.as_view()),
	url(r'^(?P<projectname>[\w-]+)/settings$', ProjectSettingView.as_view()),
	url(r'^project/(?P<name>[\w-]+)/$', ProjectView.as_view()),
	url(r'^project/(?P<projectname>[\w-]+)/import', UploadReportView.as_view()),
	url(r'^project/(?P<projectname>[\w-]+)/(?P<filename>.*)$', FileView.as_view()),
]
