# Generated by Django 3.2.19 on 2024-08-08 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generales', '0024_subcategoria3'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subcategoria3',
            old_name='user',
            new_name='subcategoria',
        ),
    ]