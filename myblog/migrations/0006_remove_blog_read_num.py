# Generated by Django 2.1.7 on 2019-04-08 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0005_readnum'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='read_num',
        ),
    ]