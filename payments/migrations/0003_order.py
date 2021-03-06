# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-16 15:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('showcase', '0003_remove_product_order'),
        ('payments', '0002_delete_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid', models.BooleanField(default=False)),
                ('count', models.SmallIntegerField(default=1)),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='showcase.Product')),
            ],
        ),
    ]
