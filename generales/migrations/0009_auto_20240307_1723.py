# Generated by Django 3.2.19 on 2024-03-07 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generales', '0008_remove_noticias_categoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='nosotros',
            name='imagen_jus',
            field=models.FileField(blank=True, upload_to='imagenes/', verbose_name='Imagen-justificacion'),
        ),
        migrations.AddField(
            model_name='nosotros',
            name='imagen_obj',
            field=models.FileField(blank=True, upload_to='imagenes/', verbose_name='Imagen-objetivos'),
        ),
        migrations.AddField(
            model_name='nosotros',
            name='imagen_users',
            field=models.FileField(blank=True, upload_to='imagenes/', verbose_name='Imagen-usuarios'),
        ),
        migrations.AddField(
            model_name='nosotros',
            name='imagen_vision',
            field=models.FileField(blank=True, upload_to='imagenes/', verbose_name='Imagen-vision'),
        ),
    ]
