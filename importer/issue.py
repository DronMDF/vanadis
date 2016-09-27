import codecs
from django.shortcuts import get_object_or_404
from base.models import Project
from importer.Report import Report
from importer.ReportStorage import ReportStorage
from importer.Repository import Repository


def uploadReport(projectname, report_stream):
	project = get_object_or_404(Project, name=projectname)
	repo = Repository(project)
	storage = ReportStorage(project, repo)
	report = Report(codecs.getreader('utf8')(report_stream))
	storage.importReport(report)
