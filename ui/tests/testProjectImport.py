from io import StringIO
from django.test import Client, TestCase
from base.models import Project


class TestImportUi(TestCase):
	def testWrongGitRepoReturn503(self):
		# Given
		Project.objects.all().delete()
		Project.objects.create(name='xxx', repo_url='git://none/none.git')
		# When
		response = Client().post('/xxx/import', data={'report': StringIO('xxx')})
		# Then
		self.assertEqual(response.status_code, 503)
