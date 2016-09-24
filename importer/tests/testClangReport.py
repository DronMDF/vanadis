from io import StringIO
from django.test import Client, TestCase
from base.models import Issue, Project


class TestClangImport(TestCase):
	def testImportSimpleWarning(self):
		# Given
		Project.objects.all().delete()
		name = 'clang-project'
		Project.objects.create(name=name)
		log = StringIO('\n'.join([
			'pid_output.c:101:30: warning: implicit conversion',
			'    else if (ftruncate(fd, pidsize) < 0)']))
		# When
		response = Client().post('/ui/project/%s/import' % name, data={'report': log})
		# Then
		issue = Issue.objects.get(project__name=name)
		self.assertEqual(issue.file.path, 'pid_output.c')
		self.assertEqual(issue.line, 101)
		self.assertEqual(issue.position, 30)
		self.assertEqual(issue.text, 'warning: implicit conversion')
		self.assertEqual(issue.code, '    else if (ftruncate(fd, pidsize) < 0)')

	def testImportLogWithDublicates(self):
		# Given
		Project.objects.all().delete()
		name = 'clang-project'
		Project.objects.create(name=name)
		log = StringIO('\n'.join([
			'dir/pid_output.c:101:30: warning: implicit conversion',
			'    else if (ftruncate(fd, pidsize) < 0)',
			'./pid_output.c:101:30: warning: implicit conversion',
			'    else if (ftruncate(fd, pidsize) < 0)',
			'../pid_output.c:101:30: warning: implicit conversion',
			'    else if (ftruncate(fd, pidsize) < 0)']))
		# When
		response = Client().post('/ui/project/%s/import/' % name, data={'report': log})
		# Then
		issue = Issue.objects.filter(project__name=name)
		self.assertEqual(len(issue), 1)
