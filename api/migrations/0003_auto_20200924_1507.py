# Generated by Django 3.0.5 on 2020-09-24 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200924_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='description',
        ),
        migrations.RemoveField(
            model_name='title',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='title',
            name='rating',
        ),
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.IntegerField(),
        ),
    ]
