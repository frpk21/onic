from urllib.parse import urlparse, parse_qs

from django.db import models
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from generales.choices import OrderNews, LinkType


# Create your models here.

class ClaseModelo(models.Model):
    activo = models.BooleanField(default=True)
    create = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

class Categoria_multimedia(ClaseModelo):
    nombre = models.CharField(max_length=100, help_text='Categoría multimedia', unique=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        super(Categoria_multimedia, self).save()

    class Meta:
        verbose_name_plural = "Categorías Multimedia"


class Categoria(ClaseModelo):
    parent = models.ForeignKey('generales.Categoria', verbose_name=_('Categoria'), on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100, help_text='Categoría')
    imagen = models.FileField("Imagen categoria", upload_to="imagenes/categorias", null=True, blank=True)
    url = models.CharField(max_length=500, help_text='URL', null=True, blank=True)
    orden = models.IntegerField(default=0)
    link_type = models.CharField(max_length=7, choices=LinkType.choices, null=True, default=LinkType.NONE)

    def __str__(self):
        return f'{self.parent} | {self.nombre}' if self.parent else f'{self.nombre}'

    class Meta:
        verbose_name_plural = "Categorías"
        unique_together = ('parent', 'nombre')
        ordering = ('orden',)


class SubCategoria(ClaseModelo):
    """
    TODO: Este modelo ya no es necesario, puede ser eliminado
    """
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, help_text='Descripción de la sub categoría')
    imagen = models.FileField("Imagen categoria (1920x1042 px)", upload_to="imagenes/categorias",default="")
    url = models.CharField(max_length=100, help_text='Url ')
    pestana_nueva = models.BooleanField(default=False)
    orden = models.IntegerField(default=0, blank=True, null=False)

    def __str__(self):
        return '{} | {}'.format(self.categoria.nombre,self.nombre)

    class Meta:
        verbose_name_plural = "Sub Categorías"
        unique_together = ('categoria', 'nombre')


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
    """
    TODO: el campo "subcategoria" ya no es necesario, puede ser eliminado
    """
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE, null=True, blank=True)
    categoria = models.ForeignKey('generales.Categoria', on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField('Fecha de publicación', blank=True, null=True, default=datetime.now)
    titulo = models.CharField(help_text='Título de la noticia', blank=False, null=False, max_length=200)
    subtitulo = models.CharField(help_text='Sub título de la noticia', blank=False, null=False, max_length=500)
    descripcion = RichTextField(max_length=15000, blank=True, null=True)
    archivo_audio = models.FileField("Archivo Audio", upload_to="audio/", blank=True, null=True, default='')
    orden = models.IntegerField(choices=OrderNews.choices, default=OrderNews.CAROUSEL, blank=False, null=False)
    imagen = models.FileField("Imagen Destacado", upload_to="imagenes/", blank=False, null=False)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default='')
    fuente = models.CharField(help_text='Fuente noticia', blank=True, null=True, max_length=50, default="SMT")
    html = models.TextField(max_length=10000, default="", blank=True, null=True)
    pdf = models.FileField("Archivo PDF", upload_to="pdf/", blank=True, null=True, default='')
    slug = models.SlugField(blank=True, null=True, max_length=250)
    
    def __str__(self):
        return '{}'.format(self.titulo)

    def save(self):
        self.slug = slugify(self.titulo)
        super(Noticias, self).save()

    class Meta:
        verbose_name_plural = "Noticias"

class Mapas(ClaseModelo):
    tema = models.CharField(help_text='Título del tema de mapas', blank=False, null=False, max_length=200)
    fecha = models.DateField('Fecha de publicación', blank=True, null=True, default=datetime.now)
    descripcion = models.CharField(help_text='Descripión', blank=False, null=False, max_length=400)
    imagen = models.FileField("Imagen tema mapa Catalogo(450x370 px)", upload_to="imagenes/mapas",default="")
    imagen2 = models.FileField("Imagen tema mapa Grande", upload_to="imagenes/mapas",default="")
    slug = models.SlugField(blank=True,null=True, max_length=250)

    def __str__(self):
        return '{}'.format(self.tema)

    def save(self):
        self.slug = slugify(self.tema)
        super(Mapas, self).save()

    class Meta:
        verbose_name_plural = "Mapas (Temas)"

class MapasDetalle(ClaseModelo):
    mapa=models.ForeignKey(Mapas, on_delete=models.CASCADE, default=0, null=False, blank=False)
    fecha = models.DateField('Fecha de publicación', blank=True, null=True, default=datetime.now)
    titulo = models.CharField(help_text='Título de la noticia', blank=False, null=False, max_length=200)
    subtitulo = models.CharField(help_text='Sub título de la noticia', blank=False, null=False, max_length=500)
    imagen = models.FileField("Imagen mapa (770x450 px)", upload_to="mapas/", blank=False, null=False)
    imagen2 = models.FileField("Imagen tema mapa Grande", upload_to="imagenes/mapas",default="")
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,default='')
    fuente = models.CharField(help_text='Fuente noticia', blank=True, null=True, max_length=50, default="SMT")
    html = models.TextField(max_length=10000, default="", blank=True, null=True)
    pdf = models.FileField("Archivo PDF", upload_to="pdf/", blank=True, null=True, default='')
    slug = models.SlugField(blank=True,null=True, max_length=250)

    def __str__(self):
        return '{}'.format(self.titulo)

    def save(self):
        self.slug = slugify(self.titulo)
        super(MapasDetalle, self).save()

    class Meta:
        verbose_name_plural = "Mapas Detalle"

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
    categoria_multimedia = models.ForeignKey(Categoria_multimedia, on_delete=models.CASCADE, default=0, null=False,blank=False)
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
    imagen = models.FileField("Imagen Destacado", upload_to="imagenes/", blank=False, null=False)
    fecha = models.DateField('Fecha de publicación', blank=True, null=True, default=datetime.now)
    titulo = models.CharField(help_text='Título de la noticia', blank=False, null=False, max_length=200)
    descripcion = RichTextField(max_length=15000, blank=True, null=True)
    archivo_audio = models.FileField("Archivo Audio", upload_to="audio/podcast/", blank=True, null=True, default='')

    def __str__(self):
        return '{}'.format(self.titulo)

    class Meta:
        verbose_name_plural = "Podcast Multimedia"


class Project(ClaseModelo):
    name = models.CharField(_("Name"), max_length=255)
    description = RichTextField(_("Description"))
    url_video = models.URLField(_("Video URL"), null=True, blank=True)
    thumbnail_image = models.ImageField(_('thumbnail image (750 x 520)'), upload_to="projects/")
    iframe_url = models.URLField(_("Iframe URL"))
    iframe_css_top = models.IntegerField(_("iframe css top"), blank=True, null=True)
    payment_gateway_url = models.URLField(_("Payment Gateway URL"))
    order = models.IntegerField(_('order'), default=0)
    slug = models.SlugField(_('slug'), unique=True, max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural = _('Projects')
        verbose_name = _('Project')
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_embed_url_video(self):
        if not self.url_video:
            return
        if 'embed' in self.url_video:
            return self.url_video
        url = urlparse(self.url_video)
        if url.hostname in ['www.youtube.com', 'youtube.com']:
            video_id = parse_qs(url.query).get('v')
            if video_id:
                return f'https://www.youtube.com/embed/{video_id[0]}'
        if url.hostname == 'youtu.be':
            video_id = url.path[1:]
            return f'https://www.youtube.com/embed/{video_id}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)
