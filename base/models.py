from django.db import models


class Project(models.Model):
	name = models.CharField(max_length=100, db_index=True)


class Issue(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	file = models.CharField(max_length=4096)
	line = models.IntegerField()
	position = models.IntegerField()
	text = models.CharField(max_length=256)
	code = models.CharField(max_length=4096)
