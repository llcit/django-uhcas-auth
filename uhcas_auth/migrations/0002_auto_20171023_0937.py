# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('uhcas_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UHCASUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('common_name', models.CharField(max_length=128, null=True, blank=True)),
                ('display_name', models.CharField(max_length=128, null=True, blank=True)),
                ('affiliation', models.CharField(max_length=254, null=True, blank=True)),
                ('department', models.CharField(max_length=254, null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='cltuhcasuser',
            name='user',
        ),
        migrations.DeleteModel(
            name='CLTUHCASUser',
        ),
    ]
