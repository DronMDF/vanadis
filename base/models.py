from django.db import models


class Project(models.Model):
	name = models.CharField(max_length=100, db_index=True)
	repo_url = models.CharField(max_length=256, null=True)


class Object(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE, db_index=True)
	oid = models.BigIntegerField(db_index=True)
	issues_count = models.IntegerField()


class Issue(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE, db_index=True)
	object = models.ForeignKey(Object, on_delete=models.CASCADE, db_index=True)
	line = models.IntegerField()
	position = models.IntegerField()
	text = models.CharField(max_length=256)
