# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-16 20:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

	initial = True

	dependencies = [
	]

	operations = [
		migrations.CreateModel(
			name='File',
			fields=[
				('id', models.AutoField(auto_created=True, primary_key=True,
					serialize=False, verbose_name='ID')),
				('path', models.CharField(max_length=4096)),
			],
		),
		migrations.CreateModel(
			name='Issue',
			fields=[
				('id', models.AutoField(auto_created=True, primary_key=True,
					serialize=False, verbose_name='ID')),
				('line', models.IntegerField()),
				('position', models.IntegerField()),
				('text', models.CharField(max_length=256)),
				('code', models.CharField(max_length=4096)),
				('file', models.ForeignKey(
					on_delete=django.db.models.deletion.CASCADE,
					to='base.File')),
			],
		),
		migrations.CreateModel(
			name='Project',
			fields=[
				('id', models.AutoField(auto_created=True, primary_key=True,
					serialize=False, verbose_name='ID')),
				('name', models.CharField(db_index=True, max_length=100)),
			],
		),
		migrations.AddField(
			model_name='issue',
			name='project',
			field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
				to='base.Project'),
		),
		migrations.AddField(
			model_name='file',
			name='project',
			field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
				to='base.Project'),
		),
	]
