# Generated by Django 3.2.19 on 2024-08-11 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generales', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mapasdetalle',
            name='autor',
        ),
        migrations.RemoveField(
            model_name='mapasdetalle',
            name='mapa',
        ),
        migrations.DeleteModel(
            name='Mapas',
        ),
        migrations.DeleteModel(
            name='MapasDetalle',
        ),
    ]