from django.urls import path, re_path
from generales import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^$', views.HomeView, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='generales/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('loginunlock/', auth_views.LoginView.as_view(template_name='generales/lock.html'), name='loginunlock'),
    path('noticias/seccion/<int:pk>', views.SeccionView, name="seccion"),
    path('multimedia', views.MultimediaView, name="multimedia"),
    path('multimedia2/<int:pk>', views.Multimedia2View, name="multimedia-s"),
    path('noticias/subseccion/<int:pk>', views.SubSeccionView, name="subseccion"),
    path('noticia/detalle/<slug>', views.DetalleView, name="detalle"),
    path('noticia/detalle_img/<int:pk>/<int:tarea>', views.DetalleImgView, name="detalle_img"),
    path('contacto', views.ContactView.as_view(), name="contact"),
    path('nosotros', views.NosotrosView, name="nosotros"),
    path('team', views.EquipoView, name="team"),
    path('post/<int:pk>', views.PublicacionesView, name="public"),
    path('maps/view/<slug>', views.VerMapaView, name="ver_mapa"),
    path('modulos/<int:pk>', views.ModulosView, name="modulos"),
    path('news/bol/', views.BoletinesView, name="boletines"),
    path('news/maps1/<slug>', views.MapasDetalleView, name="mapas1"),
    path('news/maps/', views.Mapas0View, name="mapas0"),
    path('news/maps/<int:pk>', views.MapsGalleryGroupView, name="maps_gallery_group"),
    # project urls
    path('donation/projects/', views.ProjectListView.as_view(), name="project_list"),
    path('donation/project/<slug:slug>/', views.ProjectDetailView.as_view(), name="project_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
