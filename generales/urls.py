from django.urls import include, path
from generales import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.HomeView, name='home'),
    path('noticias/seccion/<int:pk>', views.SeccionView, name="seccion"),
    path('noticias/subseccion/<int:pk>', views.SubSeccionView, name="subseccion"),
    path('noticia/detalle/<slug>', views.DetalleView, name="detalle"),
    path('contacto', views.ContactView.as_view(), name="contact"),
    path('nosotros', views.NosotrosView, name="Nosotros"),
    path('update/', views.ajax_update, name='upd'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
