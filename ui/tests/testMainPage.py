from django.test import Client, TestCase
from base.models import File, Issue, Project


class TestMainPage(TestCase):
	def testProjectListShowOnMainPage(self):
		# Given
		Project.objects.all().delete()
		Project.objects.create(name='test1')
		Project.objects.create(name='test2')
		# When
		response = Client().get('/')
		# Then
		self.assertEqual(response.status_code, 200)
		text = response.content.decode('utf-8')
		self.assertIn('test1', text)
		self.assertIn('test2', text)

	def testProjectProblemCounter(self):
		# Given
		Project.objects.all().delete()
		tp1 = Project.objects.create(name='test1')
		tp2 = Project.objects.create(name='test2')
		file1 = File.objects.create(project=tp1, path='tp1')
		file2 = File.objects.create(project=tp2, path='tp2')
		Issue.objects.create(project=tp1, file=file1, line=0, position=0)
		Issue.objects.create(project=tp1, file=file1, line=0, position=0)
		Issue.objects.create(project=tp2, file=file2, line=0, position=0)
		# When
		response = Client().get('/')
		# Then
		self.assertEqual(response.status_code, 200)
		text = response.content.decode('utf-8')
		self.assertRegex(text, 'test1[^1]+2')		# 2 issue
		self.assertRegex(text, 'test2[^2]+1')		# 1 issue
