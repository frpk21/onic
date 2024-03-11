# Generated by Django 3.2.19 on 2024-03-10 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generales', '0010_auto_20240308_0840'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activo', models.BooleanField(default=True)),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
                ('nombre', models.CharField(help_text='Nombre colaborador', max_length=150)),
                ('fb', models.CharField(blank=True, default='', max_length=300, verbose_name='FaceBook')),
                ('tw', models.CharField(blank=True, default='', max_length=300, verbose_name='Twitter')),
                ('ln', models.CharField(blank=True, default='', max_length=300, verbose_name='Linkedin')),
                ('imagen', models.FileField(blank=True, upload_to='equipo/', verbose_name='Imagen 320 x 320px')),
            ],
            options={
                'verbose_name_plural': 'Equipo',
            },
        ),
    ]
