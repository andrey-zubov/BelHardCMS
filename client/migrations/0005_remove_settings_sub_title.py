# Generated by Django 2.2.5 on 2019-10-03 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_auto_20191002_2147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settings',
            name='sub_title',
        ),
    ]
