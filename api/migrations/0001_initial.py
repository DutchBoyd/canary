# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-10 14:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='BadEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('description', models.TextField()),
                ('loss', models.FloatField()),
                ('year', models.IntegerField()),
            ],
            options={
                'ordering': ['year', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Contributions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=140)),
                ('subcategory', models.CharField(max_length=140)),
                ('year', models.IntegerField()),
                ('amount', models.FloatField()),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Asset')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('value', models.FloatField()),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Country')),
            ],
            options={
                'ordering': ['year'],
            },
        ),
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='data',
            name='index',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Index'),
        ),
        migrations.AddField(
            model_name='badevent',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Country'),
        ),
        migrations.AddField(
            model_name='asset',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Country'),
        ),
        migrations.AlterUniqueTogether(
            name='data',
            unique_together=set([('country', 'index', 'year')]),
        ),
        migrations.AlterUniqueTogether(
            name='asset',
            unique_together=set([('country', 'name')]),
        ),
    ]
