# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-27 19:23
from django.db import migrations, models


class Migration(migrations.Migration):
	dependencies = [
		('base', '0002_auto_20160917_1030'),
	]

	operations = [
		migrations.AddField(
			model_name='project',
			name='repo_url',
			field=models.CharField(max_length=256, null=True),
		),
	]
