from django.contrib import admin

from generales.models import Noticias, Suscribir, VideoSMT, Contacto, Nosotros, Categoria, SubCategoria, Mapas, Mapas1, Equipo, Imagenes, Videos, Podcast, Categoria_multimedia

from django.contrib.admin.widgets import AutocompleteSelect

import random


class NoticiasAdmin(admin.ModelAdmin):

    list_display = ('titulo', 'subtitulo', 'fecha', 'orden', 'imagen', 'modificado', 'subcategoria', 'activo', )
    fields = ['subcategoria', 'titulo', 'subtitulo', 'fecha', ('orden', 'imagen'), 'descripcion', 'archivo_audio', 'fuente', 'html', 'pdf', 'activo']
    exclude = ('slug','autor', 'modificado', 'vistas',)
    ordering = ('orden', 'titulo', 'fecha',)
    search_fields = ('titulo','subtitulo','fecha', )
    list_filter = ('subcategoria__categoria','subcategoria', 'modificado', 'orden', 'fecha',)

    class Meta:
        model = Noticias

    def save_model(self, request, obj, form, change):
        obj.autor = request.user
        obj.save()



class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'imagen',)
    ordering = ('id', )

    class Meta:
        model = Categoria

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
       return False

class SubCategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'categoria', 'nombre', 'imagen',)
    ordering = ('id', )
    list_filter = ('categoria',)

    class Meta:
        model = SubCategoria

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
       return False

class MapasAdmin(admin.ModelAdmin):
    list_display = ('imagen',)
    ordering = ('imagen', )

    class Meta:
        model = Mapas

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

class Mapas1Admin(admin.ModelAdmin):
    list_display = ('titulo', 'subtitulo', 'fecha', 'imagen', 'modificado', 'mapa', 'activo', )
    fields = ['mapa', 'titulo', 'subtitulo', 'fecha', 'imagen (770x450 px)', 'fuente', 'html', 'pdf', 'activo']
    exclude = ('slug','autor', 'modificado', )
    ordering = ('titulo', 'fecha',)
    search_fields = ('titulo','subtitulo','fecha', )
    list_filter = ('mapa', 'modificado', 'fecha',)

    class Meta:
        model = Mapas1

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

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(SubCategoria, SubCategoriaAdmin)
admin.site.register(Mapas, MapasAdmin)
admin.site.register(Mapas1, Mapas1Admin)
admin.site.register(Noticias, NoticiasAdmin)
admin.site.register(VideoSMT, VideoSMTAdmin)
admin.site.register(Nosotros, NosotrosAdmin)
admin.site.register(Contacto, ContactoAdmin)
admin.site.register(Equipo, EquipoAdmin)
admin.site.register(Imagenes, ImagenesAdmin)
admin.site.register(Videos, VideosAdmin)
admin.site.register(Podcast, PodcastAdmin)
admin.site.register(Categoria_multimedia)
