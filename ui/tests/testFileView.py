from django.test import Client, TestCase
from base.models import File, Issue, Project


class TestFileView(TestCase):
	def testViewShouldReturnByLineContext(self):
		# Given
		Project.objects.all().delete()
		p = Project.objects.create(name='ff')
		xxx = File.objects.create(project=p, path='xxx')
		Issue.objects.create(project=p, file=xxx, code='aaa',
				line=7, position=5, text='All bad')
		Issue.objects.create(project=p, file=xxx, code='aaa',
				line=7, position=10, text='End bad')
		# When
		response = Client().get('/ff/xxx')
		# Then
		sc = response.context['sourcecode']
		self.assertEqual(sc[0]['code'], 'aaa')
		self.assertEqual(sc[0]['line'], 7)
		self.assertEqual(sc[0]['issues'][0]['position'], 10)
		self.assertEqual(sc[0]['issues'][1]['position'], 5)
