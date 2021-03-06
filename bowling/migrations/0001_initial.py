# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-14 07:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Frame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll1', models.IntegerField(null=True)),
                ('roll2', models.IntegerField(null=True)),
                ('roll3', models.IntegerField(null=True)),
                ('strike', models.BooleanField(default=False)),
                ('spare', models.BooleanField(default=False)),
                ('score', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('score', models.IntegerField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='frame',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bowling.Player'),
        ),
    ]
