from django.shortcuts import get_object_or_404
from base.models import Project
from importer.Report import Report
from importer.ReportStorage import ReportStorage


def uploadReport(projectname, report_text):
	project = get_object_or_404(Project, name=projectname)
	storage = ReportStorage(project)
	report = Report(b''.join(report_text.chunks()).decode('utf8'))
	storage.importReport(report)
