from django.urls import include, path
from visor import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('update/capas/', views.ajax_updateCapas.as_view(), name='update_capas'),
    path('visor/',views.Visor.as_view(), name='visor'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
