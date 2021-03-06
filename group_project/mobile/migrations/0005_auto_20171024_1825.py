# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-24 18:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile', '0004_grouplocalization_locationdensity'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyMatrix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('group', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='grouplocalization',
            name='group',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='grouplocalization',
            name='timestamp',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='locationdensity',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]
