# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-10 03:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('riotapi_static', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeagueMainsUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('joined', models.DateTimeField(auto_now_add=True)),
                ('summoner', models.CharField(max_length=255, unique=True)),
                ('region', models.CharField(max_length=255)),
                ('language', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ChampionsInChampionList',
            fields=[
                ('pk_id', models.AutoField(primary_key=True, serialize=False)),
                ('fk_champion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riotapi_static.Champion')),
            ],
        ),
        migrations.CreateModel(
            name='UserChampionList',
            fields=[
                ('pk_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('is_public', models.BooleanField(default=False)),
                ('fk_leaguemainsuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='championsinchampionlist',
            name='fk_userchampionlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leaguemains.UserChampionList'),
        ),
    ]