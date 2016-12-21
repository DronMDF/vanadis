from django.test import TestCase
from base.models import Object, Project


class TestModels(TestCase):
	def testObjectCleanupOnProjectDelete(self):
		# Given
		project = Project.objects.create(name='deleted')
		Object.objects.create(project=project, oid=777, issues_count=0)
		# When
		project.delete()
		# Then
		self.assertEqual(Object.objects.filter(oid=777).count(), 0)
