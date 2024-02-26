from django.contrib import admin

from generales.models import Noticias, Suscribir, VideoSMT, Contacto, Nosotros, Categoria, SubCategoria

from django.contrib.admin.widgets import AutocompleteSelect

import random


class NoticiasAdmin(admin.ModelAdmin):

    list_display = ('subcategoria', 'titulo', 'subtitulo', 'orden', 'imagen', 'modificado','activo', )
    fields = ['subcategoria', 'titulo', 'subtitulo', ('orden', 'imagen'), 'descripcion', 'archivo_audio', 'fuente', 'html', 'pdf', 'activo']
    exclude = ('slug','autor', 'modificado', 'vistas',)
    ordering = ('orden', 'titulo', '-modificado',)
    search_fields = ('titulo','subtitulo')
    list_filter = ('modificado', 'orden')

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

class SubCategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'categoria', 'nombre', 'imagen',)
    ordering = ('id', )

    class Meta:
        model = SubCategoria

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


class VideoSMTAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'url_video',)
    ordering = ('titulo', )

    class Meta:
        model = VideoSMT

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

class NosotrosAdmin(admin.ModelAdmin):
    list_display = ('descripcion','vision', 'justificacion', 'objetivos', 'usuarios')

    class Meta:
        model = Nosotros

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

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(SubCategoria, SubCategoriaAdmin)
admin.site.register(Noticias, NoticiasAdmin)
admin.site.register(VideoSMT, VideoSMTAdmin)
admin.site.register(Nosotros, NosotrosAdmin)
admin.site.register(Contacto, ContactoAdmin)

