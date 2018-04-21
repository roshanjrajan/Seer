# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-21 00:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_auto_20180421_0027'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='id',
            field=models.AutoField(auto_created=True, default='1', primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='account',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]