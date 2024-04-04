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

class Categoria_multimedia(ClaseModelo):
    nombre = models.CharField(max_length=100, help_text='Categoría multimedia', unique=True)
    imagen = models.FileField("Imagen categoria multimedia", upload_to="imagenes/categorias",default="")

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        super(Categoria_multimedia, self).save()

    class Meta:
        verbose_name_plural = "Categorías Multimedia"

class Categoria(ClaseModelo):
    nombre = models.CharField(max_length=100, help_text='Categoría', unique=True)
    imagen = models.FileField("Imagen categoria", upload_to="imagenes/categorias",default="")

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
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
        super(SubCategoria, self).save()

    class Meta:
        verbose_name_plural = "Sub Categorías"
        unique_together = ('categoria','nombre')


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
    imagen = models.FileField("Imagen 1020x 1042px", upload_to="imagenes/", blank=True, null=False)
    imagen_vision = models.FileField("Imagen-vision 470x610px", upload_to="imagenes/", blank=True, null=False)
    imagen_jus = models.FileField("Imagen-justificacion 500x382px", upload_to="imagenes/", blank=True, null=False)
    imagen_obj = models.FileField("Imagen-objetivos 500x30px", upload_to="imagenes/", blank=True, null=False)
    imagen_users = models.FileField("Imagen-usuarios 500x370", upload_to="imagenes/", blank=True, null=False)

    def __str__(self):
        return '{}'.format(self.id)

    def save(self):
        super(Nosotros, self).save()

    class Meta:
        verbose_name_plural = "Nosotros"

class Equipo(ClaseModelo):
    nombre = models.CharField(max_length=150, help_text='Nombre colaborador')
    cargo = models.CharField(max_length=70, help_text='Cargo')
    perfil = RichTextField('Perfil', max_length=2000, blank=True, null=False, default='')
    fb = models.CharField('FaceBook', max_length=300, blank=True, null=False, default='')
    tw = models.CharField('Twitter', max_length=300, blank=True, null=False, default='')
    ln = models.CharField('Linkedin', max_length=300, blank=True, null=False, default='')
    imagen = models.FileField("Imagen 320 x 320px", upload_to="equipo/", blank=True, null=False)
    orden = models.CharField(max_length=4, help_text='Orden')

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        super(Equipo, self).save()

    class Meta:
        verbose_name_plural = "Equipo"

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
    subcategoria=models.ForeignKey(SubCategoria, on_delete=models.CASCADE, default=0, null=False, blank=False)
    fecha = models.DateField('Fecha de publicación', blank=True, null=True, default=datetime.now)
    titulo = models.CharField(help_text='Título de la noticia', blank=False, null=False, max_length=200)
    subtitulo = models.CharField(help_text='Sub título de la noticia', blank=False, null=False, max_length=500)
    descripcion = RichTextField(max_length=15000, blank=True, null=True)
    archivo_audio = models.FileField("Archivo Audio", upload_to="audio/", blank=True, null=True, default='')
    CHOICES = ((0,'Carrusel'),(1,'Noticia 1'),(2,'Novedades 2'),(3,'Boletines 3'),(4,'Mediateca 4'), (5,'General'))
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

class Imagenes(ClaseModelo):
    categoria_multimedia=models.ForeignKey(Categoria_multimedia, on_delete=models.CASCADE, default=0, null=False, blank=False)
    fecha = models.DateField('Fecha de publicación', blank=True, null=True, default=datetime.now)
    titulo = models.CharField(help_text='Título de la noticia', blank=False, null=False, max_length=200)
    descripcion = RichTextField(max_length=15000, blank=True, null=True)
    imagen = models.FileField("Imagen Destacado", upload_to="imagenes/", blank=False, null=False)
    
    def __str__(self):
        return '{}'.format(self.titulo)

    class Meta:
        verbose_name_plural = "Imagenes Multimedia"

class Videos(ClaseModelo):
    categoria_multimedia=models.ForeignKey(Categoria_multimedia, on_delete=models.CASCADE, default=0, null=False, blank=False)
    fecha = models.DateField('Fecha de publicación', blank=True, null=True, default=datetime.now)
    titulo = models.CharField(help_text='Título de la noticia', blank=False, null=False, max_length=200)
    descripcion = RichTextField(max_length=15000, blank=True, null=True)
    html = models.TextField(max_length=10000, default="", blank=True, null=True)
    
    def __str__(self):
        return '{}'.format(self.titulo)

    class Meta:
        verbose_name_plural = "Videos Multimedia"

class Podcast(ClaseModelo):
    categoria_multimedia=models.ForeignKey(Categoria_multimedia, on_delete=models.CASCADE, default=0, null=False, blank=False)
    fecha = models.DateField('Fecha de publicación', blank=True, null=True, default=datetime.now)
    titulo = models.CharField(help_text='Título de la noticia', blank=False, null=False, max_length=200)
    descripcion = RichTextField(max_length=15000, blank=True, null=True)
    archivo_audio = models.FileField("Archivo Audio", upload_to="audio/", blank=True, null=True, default='')
    
    def __str__(self):
        return '{}'.format(self.titulo)

    class Meta:
        verbose_name_plural = "Podcast Multimedia"