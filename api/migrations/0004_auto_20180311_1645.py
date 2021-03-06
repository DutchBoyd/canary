# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-11 16:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_country_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstimatedRisk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('value', models.CharField(choices=[('HIGH', 'High Risk'), ('MODERATE', 'Moderate Risk')], max_length=8)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Country')),
            ],
            options={
                'ordering': ['year'],
            },
        ),
        migrations.AlterModelOptions(
            name='risk',
            options={'ordering': ['year']},
        ),
        migrations.AlterUniqueTogether(
            name='risk',
            unique_together=set([('country', 'year')]),
        ),
        migrations.AlterUniqueTogether(
            name='estimatedrisk',
            unique_together=set([('country', 'year')]),
        ),
    ]
