import codecs
from django.shortcuts import get_object_or_404
from base.models import Project
from importer.Report import Report
from importer.ReportStorage import ReportStorage


def uploadReport(projectname, report_stream):
	project = get_object_or_404(Project, name=projectname)
	storage = ReportStorage(project)
	report = Report(codecs.getreader('utf8')(report_stream))
	storage.importReport(report)
