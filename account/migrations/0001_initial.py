# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='Email Address', db_index=True)),
                ('first_name', models.CharField(max_length=32, null=True, verbose_name='First Name', blank=True)),
                ('last_name', models.CharField(max_length=32, null=True, verbose_name='Last Name', blank=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='Is Active')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'auth_user',
            },
        ),
    ]
