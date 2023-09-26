from django.db import models
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from multiselectfield import MultiSelectField


# Create your models here.

class ClaseModelo(models.Model):
    activo = models.BooleanField(default=True)
    create = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

"""
class Categoria(ClaseModelo):
    nombre = models.CharField(max_length=100, help_text='Categoría', unique=True)
    imagen = models.FileField("Imagen categoria", upload_to="imagenes/categorias",default="")

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.upper()
        super(Categoria, self).save()

    class Meta:
        verbose_name_plural = "Categorías"

class SubCategoria(ClaseModelo):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, help_text='Descripción de la sub categoría')
    imagen = models.FileField("Imagen categoria", upload_to="imagenes/categorias",default="")

    def __str__(self):
        return '{}: {}'.format(self.categoria.nombre,self.nombre)

    def save(self):
        self.nombre = self.nombre.upper()
        super(SubCategoria, self).save()

    class Meta:
        verbose_name_plural = "Sub Categorías"
        unique_together = ('categoria','nombre')
"""

class Suscribir(ClaseModelo):
    email = models.CharField(max_length=200, help_text='eMail', unique=True)

    def __str__(self):
        return '{}'.format(self.email)

    class Meta:
        verbose_name_plural = "Suscribirse"


class Nosotros(ClaseModelo):
    descripcion = RichTextField('Descripción', max_length=10000, blank=True, null=False, default='')
    vision = RichTextField('Visión', max_length=10000, blank=True, null=False, default='')
    justificacion = RichTextField('Justificación', max_length=10000, blank=True, null=False, default='')
    objetivos = RichTextField(max_length=10000, blank=True, null=False, default='')
    usuarios = RichTextField(max_length=10000, blank=True, null=False, default='')

    def __str__(self):
        return '{}'.format(self.idEmisora)

    def save(self):
        super(Nosotros, self).save()

    class Meta:
        verbose_name_plural = "Nosotros"


class VideoSMT(ClaseModelo):
    titulo = models.CharField(blank=False, null=False, max_length=200)
    url_video = models.TextField("ingrese la URL del vídeo.",max_length=250, blank=False, null=False)

    def __str__(self):
        return '{}'.format(self.titulo)

    def save(self):
        self.titulo = self.titulo.upper()
        super(VideoSMT, self).save()

    class Meta:
        verbose_name_plural = "Video SMT"

class Contacto(ClaseModelo):
    nombre = models.CharField(help_text='Nombre y Apellidos', blank=False, null=False, max_length=200)
    email = models.CharField(help_text='Correo electrónico', blank=False, null=False, max_length=200)
    telefono = models.CharField(help_text='Teléfono de contacto', blank=True, null=True, max_length=100, default="")
    ciudad = models.CharField(help_text='Ciudad de residencia', blank=True, null=True, max_length=100, default="")
    pais = models.CharField(help_text='País de residencia', blank=True, null=True, max_length=100, default="")
    textoMensage = models.TextField(help_text='Mensage', blank=False, null=False, max_length=10000)

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.upper()
        self.nombre = self.ciudad.upper()
        self.nombre = self.pais.upper()
        super(Contacto, self).save()

    class Meta:
        verbose_name_plural = "Contactos"

class Noticias(ClaseModelo):
    titulo = models.CharField(help_text='Título de la noticia', blank=False, null=False, max_length=200)
    subtitulo = models.CharField(help_text='Sub título de la noticia', blank=False, null=False, max_length=500)
    descripcion = RichTextField(max_length=15000, blank=True, null=True)
    archivo_audio = models.FileField("Archivo Audio", upload_to="audio/", blank=True, null=True, default='')
    CHOICES = ((0,'Carrusel'),(1,'Noticia 1'),(2,'Novedades 2'),(3,'Boletines 3'),(4,'Mediateca 4'))
    orden = models.IntegerField(choices=CHOICES, default=0, blank=False, null=False)
    imagen = models.FileField("Imagen Destacado", upload_to="imagenes/", blank=False, null=False)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,default='')
    fuente = models.CharField(help_text='Fuente noticia', blank=True, null=True, max_length=50, default="SMT")
    html = models.TextField(max_length=10000, default="", blank=True, null=True)
    pdf = models.FileField("Archivo PDF", upload_to="pdf/", blank=True, null=True, default='')
    slug = models.SlugField(blank=True,null=True, max_length=250)
    
    def __str__(self):
        return '{}'.format(self.titulo)

    def save(self):
        self.slug = slugify(self.titulo)
        super(Noticias, self).save()

    class Meta:
        verbose_name_plural = "Noticias"

class Comentario(ClaseModelo):
    noticia = models.ForeignKey(Noticias, on_delete=models.CASCADE, default=0, null=False, blank=False)
    comentario = models.TextField(max_length=10000, blank=True, null=True)
    nombre = models.CharField(blank=False, null=False, max_length=200)
    email = models.CharField(blank=False, null=False, max_length=200)

    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        verbose_name_plural = "Comentarios"
