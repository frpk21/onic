from django.contrib import admin

from generales.models import Noticias, Suscribir, VideoSMT, Contacto, Nosotros, Categoria, SubCategoria, Equipo

from django.contrib.admin.widgets import AutocompleteSelect

import random


class NoticiasAdmin(admin.ModelAdmin):

    list_display = ('titulo', 'subtitulo', 'orden', 'imagen', 'modificado', 'subcategoria', 'activo', )
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
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
       return False

class SubCategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'categoria', 'nombre', 'imagen',)
    ordering = ('id', )

    class Meta:
        model = SubCategoria

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
       return False


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
    list_display = ('nombre', 'cargo', 'fb', 'tw', 'ln', 'imagen')

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

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(SubCategoria, SubCategoriaAdmin)
admin.site.register(Noticias, NoticiasAdmin)
admin.site.register(VideoSMT, VideoSMTAdmin)
admin.site.register(Nosotros, NosotrosAdmin)
admin.site.register(Contacto, ContactoAdmin)
admin.site.register(Equipo, EquipoAdmin)

