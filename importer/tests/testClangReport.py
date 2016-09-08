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
		response = Client().post('/import/', data={'project': name, 'log': log})
		# Then
		issue = Issue.objects.get(project__name=name)
		self.assertEqual(issue.file, 'pid_output.c')
		self.assertEqual(issue.line, 101)
		self.assertEqual(issue.position, 30)
		self.assertEqual(issue.text, 'implicit conversion')
		self.assertEqual(issue.code, '    else if (ftruncate(fd, pidsize) < 0)')
