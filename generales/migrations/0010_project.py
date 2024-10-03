# Generated by Django 5.1.1 on 2024-09-27 14:08

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generales', '0009_auto_20240902_1125'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activo', models.BooleanField(default=True)),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', ckeditor.fields.RichTextField(verbose_name='Description')),
                ('url_video', models.URLField(verbose_name='Video URL')),
                ('thumbnail_image', models.ImageField(upload_to='projects/', verbose_name='thumbnail image (750 x 520)')),
                ('iframe_url', models.URLField(verbose_name='Iframe URL')),
                ('payment_gateway_url', models.URLField(verbose_name='Payment Gateway URL')),
                ('order', models.IntegerField(default=0, verbose_name='order')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
                'ordering': ['order'],
            },
        ),
    ]