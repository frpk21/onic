# Generated by Django 3.2.19 on 2024-03-20 12:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generales', '0016_alter_noticias_orden'),
    ]

    operations = [
        migrations.AddField(
            model_name='noticias',
            name='fecha',
            field=models.DateField(blank=True, default=datetime.datetime.now, null=True, verbose_name='Fecha de publicación'),
        ),
    ]
