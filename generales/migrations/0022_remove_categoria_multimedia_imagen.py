# Generated by Django 3.2.19 on 2024-04-04 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generales', '0021_auto_20240404_1624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoria_multimedia',
            name='imagen',
        ),
    ]
