from django.contrib import admin

from generales.models import Noticias, VideoSMT, Contacto, Nosotros, Categoria, Mapas, MapasDetalle, Equipo, Imagenes, \
    Videos, Podcast, Categoria_multimedia, Project

from django.contrib.admin.widgets import AutocompleteSelect

import random


class NoticiasAdmin(admin.ModelAdmin):

    list_display = ('titulo', 'subtitulo', 'orden', 'categoria', 'activo',  'fecha',  'modificado')
    fields = ['categoria', 'titulo', 'subtitulo', 'fecha', ('orden', 'imagen'), 'descripcion', 'archivo_audio', 'fuente', 'html', 'pdf', 'activo']
    exclude = ('slug','autor', 'modificado', 'vistas',)
    ordering = ('orden', 'titulo', 'fecha',)
    search_fields = ('titulo','subtitulo','fecha', )
    list_filter = ('categoria', 'modificado', 'orden', 'fecha',)
    raw_id_fields = ('categoria',)
    list_editable = ('categoria',)

    class Meta:
        model = Noticias

    def save_model(self, request, obj, form, change):
        obj.autor = request.user
        obj.save()


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent', 'nombre', 'url',  'orden', 'link_type', 'activo')
    ordering = ('orden', 'id', 'nombre', '-parent')
    search_fields = ('nombre', 'parent__nombre', 'url')
    list_filter = ('link_type', 'parent')
    list_editable = ('nombre', 'url', 'orden', 'link_type', 'activo')
    raw_id_fields = ('parent', )

    class Meta:
        model = Categoria

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


class MapasAdmin(admin.ModelAdmin):
    list_display = ('tema', 'fecha', 'descripcion', 'imagen', 'activo')
    ordering = ('tema',)
    exclude = ('slug',)
    search_fields = ('tema', 'fecha',)
    list_filter = ('tema', 'fecha',)

    class Meta:
        model = Mapas

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


class MapasDetalleAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'subtitulo', 'fecha', 'imagen', 'imagen2','modificado', 'mapa', 'activo', )
    fields = ['mapa', 'titulo', 'subtitulo', 'fecha', 'imagen', 'imagen2','fuente', 'html', 'pdf', 'activo']
    exclude = ('slug','autor', 'modificado', )
    ordering = ('titulo', 'fecha',)
    search_fields = ('titulo','subtitulo','fecha', )
    list_filter = ('mapa', 'modificado', 'fecha',)

    class Meta:
        model = MapasDetalle

    def save_model(self, request, obj, form, change):
        obj.save()


class VideoSMTAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'url_video',)
    ordering = ('titulo', )

    class Meta:
        model = VideoSMT

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


class NosotrosAdmin(admin.ModelAdmin):
    list_display = ('descripcion','vision', 'justificacion', 'objetivos', 'usuarios','imagen', 'imagen_vision', 'imagen_jus', 'imagen_obj', 'imagen_users')

    class Meta:
        model = Nosotros

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'perfil', 'cargo', 'orden', 'fb', 'tw', 'ln', 'imagen')

    class Meta:
        model = Equipo

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'ciudad', 'pais', 'modificado','textoMensage', )
    fields = ['nombre', 'email', 'telefono', 'ciudad', 'pais', 'textoMensage', 'modificado','activo']
    ordering = ('-modificado', 'nombre', )
    search_fields = ('modificado','nombre')

    class Meta:
        model = Contacto

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


class ImagenesAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria_multimedia', 'fecha', 'imagen',)
    ordering = ('titulo', )
    list_filter = ('titulo',)

    class Meta:
        model = Imagenes

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


class VideosAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria_multimedia', 'fecha', 'html',)
    ordering = ('titulo', )
    list_filter = ('titulo',)

    class Meta:
        model = Videos

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


class PodcastAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria_multimedia', 'fecha', 'archivo_audio','imagen')
    ordering = ('titulo', )
    list_filter = ('titulo',)

    class Meta:
        model = Podcast

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'order', 'thumbnail_image', 'payment_gateway_url', 'iframe_url', 'iframe_css_top','activo')
    list_editable = ('order','name', 'thumbnail_image', 'payment_gateway_url', 'iframe_url', 'iframe_css_top', 'activo')
    exclude = ('slug',)

    class Meta:
        model = Project


admin.site.register(Categoria, CategoriaAdmin)
# admin.site.register(SubCategoria, SubCategoriaAdmin)
admin.site.register(Mapas, MapasAdmin)
admin.site.register(MapasDetalle, MapasDetalleAdmin)
admin.site.register(Noticias, NoticiasAdmin)
admin.site.register(VideoSMT, VideoSMTAdmin)
admin.site.register(Nosotros, NosotrosAdmin)
admin.site.register(Contacto, ContactoAdmin)
admin.site.register(Equipo, EquipoAdmin)
admin.site.register(Imagenes, ImagenesAdmin)
admin.site.register(Videos, VideosAdmin)
admin.site.register(Podcast, PodcastAdmin)
admin.site.register(Categoria_multimedia)
