# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-05-03 12:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dept',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='部門名稱')),
            ],
            options={
                'verbose_name': '部門',
                'verbose_name_plural': '部門',
                'db_table': 'dept',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('salary', models.IntegerField(default=None, verbose_name='工資')),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Dept')),
            ],
            options={
                'verbose_name': '人員',
                'verbose_name_plural': '人員',
                'db_table': 'person',
            },
        ),
    ]