from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse_lazy

from django.views import generic

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from generales.models import Noticias, Comentario, Contacto, VideoSMT, Nosotros, Categoria, SubCategoria, Mapas, MapasDetalle, Equipo, Podcast, Videos, Imagenes, Categoria_multimedia

from datetime import date

from django.shortcuts import render

from generales.forms import SuscribirseForm, ComentarioForm, ContactoForm
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import JsonResponse
from datetime import timedelta
import json 
import os
import folium
from folium.features import CustomIcon
from folium.plugins import Search,  MarkerCluster, FastMarkerCluster
from folium import plugins
#from geoserver.catalog import Catalog
from django.views import generic
from owslib.wms import WebMapService
from owslib.wfs import WebFeatureService
from owslib.fes import *
from owslib.etree import etree
import json
import geopandas as gpd
import requests
from pyproj import CRS
import geojson
import asyncio
from django.template.loader import render_to_string


def HomeView(request):
    #CHOICES = ((0,'Carrusel'),(1,'Noticia 1'),(2,'Novedades 2'),(3,'Boletines 3'),(4,'Mediateca 4'))
    hoy = date.today()
    carrusel = Noticias.objects.filter(orden=0).order_by('-fecha')[:3]
    noticias = Noticias.objects.filter(orden=1).last()
    video_smt = VideoSMT.objects.all().last()
    nosotros = Nosotros.objects.all().last()
    novedades = Noticias.objects.filter(orden=2).order_by('-fecha')[:7]
    #boletines = Noticias.objects.filter(orden=3).order_by('-fecha')[:10]
    
    context = {
        'hoy': hoy,
        'carrusel': carrusel,
        'noticias': noticias,
        'video_smt': video_smt,
        'nosotros': nosotros,
        'novedades': novedades,
        #'boletines': boletines,
        #'mediateca': mediateca,
        'categorias' : Categoria.objects.all().order_by('id'),
        'subcategorias': SubCategoria.objects.all().order_by('id'),
        'categorias_mul': Categoria_multimedia.objects.all(),
        'modulos': SubCategoria.objects.filter(categoria__id=20).order_by('id')
        }
    manana = hoy + timedelta(days=1)
    if request.POST.get('email'):
        form_home = SuscribirseForm(request.POST)
        if form_home.is_valid():
            post = form_home.save(commit=False)
            post.save()
            success_url=reverse_lazy("/")

            return JsonResponse(
                {
                    'content': {
                        'message': 'Gracias por suscribirse.',
                    }
                }
            )
        else:
            return JsonResponse(
                {
                    'content': {
                        'message': 'Ya ha sido registrado. Gracias!',
                    }
                }
            )
    else:
        form_home = SuscribirseForm()

    if request.POST.get('buscar'):
        buscar = (request.POST.get('buscar').upper())
        template_name="generales/search.html"
        try:
            resultado = Noticias.objects.filter(titulo__icontains=buscar).order_by('-id')
            #paginator5 = Paginator(resultado, 10)
        except:
            resultado = Noticias.objects.filter(titulo__icontains=buscar).order_by('-id')
            #paginator5 = Paginator(resultado, 10)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        #try:
        #    resultado = paginator5.page(page)
        #except (EmptyPage, InvalidPage):
        #    resultado = paginator5.page(paginator5.num_pages)

        #context['paginator5'] = paginator5
        context['form_search'] = resultado
    else:
        buscar = ''
        resultado={}
        template_name = "generales/home.html"

    context['form_home'] = form_home
    context['resultado'] = resultado

    return render(request, template_name, context)

def SeccionView(request, pk):
    template_name = 'generales/seccion.html'
    if pk == 1:
        nosotros = Nosotros.objects.all().last()
    hoy = date.today()
    categorias = Categoria.objects.all().order_by('id')
    subcategorias = SubCategoria.objects.all().order_by('id')
    seccion = Categoria.objects.get(id=pk)
    sub = SubCategoria.objects.filter(categoria__id=pk)
    noticias = Noticias.objects.filter(subcategoria__categoria__id=pk).order_by('-fecha')[:20]
    context = {'hoy': hoy, 'noticias': noticias, 'categorias_mul': Categoria_multimedia.objects.all(), 'categorias': categorias, 'subcategorias': subcategorias, 'seccion': seccion, 'sub': sub, 'modulos': SubCategoria.objects.filter(categoria__id=20).order_by('id')}

    if request.POST.get('buscar'):
        buscar = (request.POST.get('buscar').upper())
        template_name="generales/search.html"
        try:
            resultado = Noticias.objects.filter(titulo__icontains=buscar).order_by('-id')
            #paginator5 = Paginator(resultado, 10)
        except:
            resultado = Noticias.objects.filter(titulo__icontains=buscar).order_by('-id')
            #paginator5 = Paginator(resultado, 10)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        #try:
        #    resultado = paginator5.page(page)
        #except (EmptyPage, InvalidPage):
        #    resultado = paginator5.page(paginator5.num_pages)

        #context['paginator5'] = paginator5
    else:
        buscar = ''
        resultado={}

    context['resultado'] = resultado

    return render(request, template_name, context)

def NosotrosView(request):
    template_name = 'generales/nosotros.html'
    hoy = date.today()
    categorias = Categoria.objects.all().order_by('id')
    subcategorias = SubCategoria.objects.all().order_by('id')
    nosotros = Nosotros.objects.all().last()
    context = {'img_bak': SubCategoria.objects.get(id=14), 'hoy': hoy, 'nosotros': nosotros, 'categorias_mul': Categoria_multimedia.objects.all(), 'categorias': categorias, 'subcategorias': subcategorias, 'modulos': SubCategoria.objects.filter(categoria__id=20).order_by('id')}

    return render(request, template_name, context)

def EquipoView(request):
    template_name = 'generales/equipo.html'
    hoy = date.today()
    categorias = Categoria.objects.all().order_by('id')
    subcategorias = SubCategoria.objects.all().order_by('id')
    equipo = Equipo.objects.filter(activo=True).exclude(orden=0).order_by('orden')
    concejero = Equipo.objects.filter(orden=0).last()
    context = {'img_bak': SubCategoria.objects.get(id=15), 'hoy': hoy, 'categorias_mul': Categoria_multimedia.objects.all(), 'concejero': concejero, 'nosotros': Nosotros.objects.all().last(), 'equipo': equipo, 'categorias': categorias, 'subcategorias': subcategorias, 'modulos': SubCategoria.objects.filter(categoria__id=20).order_by('id')}
    return render(request, template_name, context)

def BoletinesView(request):
    template_name = 'generales/boletines.html'
    hoy = date.today()
    categorias = Categoria.objects.all().order_by('id')
    subcategorias = SubCategoria.objects.all().order_by('id')
    boletines = Noticias.objects.filter(orden=3).order_by('-fecha')
    noticias = Noticias.objects.all().order_by('-fecha')[:10]
    context = {'img_bak': SubCategoria.objects.get(id=20), 'noticias': noticias, 'hoy': hoy, 'categorias_mul': Categoria_multimedia.objects.all(), 'boletines': boletines, 'nosotros': Nosotros.objects.all().last(), 'categorias': categorias, 'subcategorias': subcategorias, 'modulos': SubCategoria.objects.filter(categoria__id=20).order_by('id')}
    return render(request, template_name, context)

def Mapas0View(request):
    template_name = 'generales/mapas0.html'
    mapas = Mapas.objects.filter(activo=True).order_by('tema')
    context = {'mapas': mapas, 'hoy': date.today(), 'categorias_mul': Categoria_multimedia.objects.all(), 'subcategorias': SubCategoria.objects.all().order_by('id'), 'nosotros': Nosotros.objects.all().last(), 'categorias': Categoria.objects.all().order_by('id'), 'modulos': SubCategoria.objects.filter(categoria__id=20).order_by('id')}
    return render(request, template_name, context)

def PublicacionesView(request, pk):
    template_name = 'generales/public.html'
    hoy = date.today()
    categorias = Categoria.objects.all().order_by('id')
    subcategorias = SubCategoria.objects.all().order_by('id')
    if pk == 23:
        publicaciones = Noticias.objects.filter(subcategoria_id=pk).order_by('id')
    else:
        publicaciones = MapasDetalle.objects.filter(mapa_id=pk, activo=True).order_by('titulo')
    c_p = Categoria.objects.get(id=14)  # 14 = Publicaciones
    context = {'pk': pk, 'hoy': hoy, 'categorias_mul': Categoria_multimedia.objects.all(), 'subcategorias': subcategorias, 'cat_p': c_p, 'nosotros': Nosotros.objects.all().last(), 'publicaciones': publicaciones, 'categorias': categorias, 'modulos': SubCategoria.objects.filter(categoria__id=20).order_by('id')}
    return render(request, template_name, context)

def ModulosView(request, pk):
    template_name = 'generales/modulos.html'
    hoy = date.today()
    categorias = Categoria.objects.all().order_by('id')
    subcategorias = SubCategoria.objects.all().order_by('id')
    #subcategorias3 = SubCategoria3.objects.filter("subcategoria_id = 25")
    modulo = SubCategoria.objects.get(id=pk)
    modulos2 = SubCategoria.objects.filter(categoria__id=20)   # 20=modulos
    noticias = Noticias.objects.filter(subcategoria__id=pk).last()
    c_p = Categoria.objects.get(id=20)  # 20 = modulos
    context = {'hoy': hoy, 'categorias_mul': Categoria_multimedia.objects.all(), 'modulos2': modulos2, 'subcategorias': subcategorias, 'cat_p': c_p, 'nosotros': Nosotros.objects.all().last(), 'noticias': noticias, 'categorias': categorias, 'modulo': modulo, 'modulos': SubCategoria.objects.filter(categoria__id=20).order_by('id')}
    return render(request, template_name, context)

def MultimediaView(request):
    template_name = 'generales/multimedia.html'
    hoy = date.today()
    categorias = Categoria.objects.all().order_by('id')
    categoria = Categoria.objects.get(id=16)
    subcategorias = SubCategoria.objects.all().order_by('id')
    multimedia = Noticias.objects.filter(subcategoria__categoria__id=16)
    catastro = multimedia.filter(subcategoria__id=33)
    censo = multimedia.filter(subcategoria__id=34)
    tiempo = multimedia.filter(subcategoria__id=35)
    mediateca = Noticias.objects.filter(orden=4).order_by('-fecha')[:3]
    c_p = Categoria.objects.get(id=16)  # 16 = Multimedia
    context = {'mediateca': mediateca, 'hoy': hoy, 'categorias_mul': Categoria_multimedia.objects.all(), 'catastro': catastro,'censo': censo,'tiempo': tiempo, 'subcategorias': subcategorias, 'cat_p': c_p, 'nosotros': Nosotros.objects.all().last(), 'multimedia': multimedia, 'categorias': categorias, 'categoria': categoria, 'modulos': SubCategoria.objects.filter(categoria__id=20).order_by('id')}
    return render(request, template_name, context)

def Multimedia2View(request, pk):
    template_name = 'generales/multimedia2.html'
    hoy = date.today()
    categorias = Categoria.objects.all().order_by('id')
    cat_multimedia = Categoria_multimedia.objects.get(id=pk)
    subcategorias = SubCategoria.objects.all().order_by('id')
    multimedia = Noticias.objects.filter(subcategoria__id=pk).order_by('-fecha')
    podcast = Podcast.objects.filter(categoria_multimedia__id=pk).order_by('-fecha')[:12]
    videos = Videos.objects.filter(categoria_multimedia__id=pk).order_by('-fecha')[:12]
    imagenes = Imagenes.objects.filter(categoria_multimedia__id=pk).order_by('-fecha')[:12]
    mediateca = Noticias.objects.filter(orden=4).order_by('-fecha')[:3]
    """
    try:
        imagenes = Imagenes.objects.filter(categoria_multimedia__id=pk).order_by('-id')[:10]
        paginator2 = Paginator(imagenes, 6)
    except:
        imagenes = Imagenes.objects.filter(categoria_multimedia__id=pk).order_by('-id')[:10]
        paginator2 = Paginator(imagenes, 6)
    try:
        page2 = int(request.GET.get('page', '1'))
    except ValueError:
        page2 = 1
    try:
        imagenes = paginator2.page(page2)
    except (EmptyPage, InvalidPage):
        imagenes = paginator2.page(paginator2.num_pages)
    """
    c_p = Categoria.objects.get(id=16)  # 16 = Multimedia
    context = {'mediateca': mediateca, 'mutlimedia': multimedia, 'podcast': podcast,'videos': videos,'imagenes': imagenes, 'hoy': hoy, 'categorias_mul': Categoria_multimedia.objects.all(), 'subcategorias': subcategorias, 'cat_p': c_p, 'nosotros': Nosotros.objects.all().last(), 'multimedia': multimedia, 'categorias': categorias, 'cat_multimedia': cat_multimedia, 'modulos': SubCategoria.objects.filter(categoria__id=20).order_by('id')}

    return render(request, template_name, context)

def SubSeccionView(request, pk):
    template_name = 'generales/seccion.html'
    hoy = date.today()
    categorias = Categoria.objects.all().order_by('id')
    subcategorias = SubCategoria.objects.all().order_by('id')
    noticias = Noticias.objects.filter(subcategoria__id=pk).order_by('-fecha')[:20]
    context = {'hoy': hoy, 'noticias': noticias, 'categorias_mul': Categoria_multimedia.objects.all(), 'categorias': categorias, 'subcategorias': subcategorias, 'seccion': SubCategoria.objects.get(id=pk), 'modulos': SubCategoria.objects.filter(categoria__id=20).order_by('id')}
    if request.POST.get('buscar'):
        buscar = (request.POST.get('buscar').upper())
        template_name="generales/search.html"
        try:
            resultado = Noticias.objects.filter(titulo__icontains=buscar).order_by('-id')
            #paginator5 = Paginator(resultado, 10)
        except:
            resultado = Noticias.objects.filter(titulo__icontains=buscar).order_by('-id')
            #paginator5 = Paginator(resultado, 10)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        #try:
        #    resultado = paginator5.page(page)
        #except (EmptyPage, InvalidPage):
        #    resultado = paginator5.page(paginator5.num_pages)

        #context['paginator5'] = paginator5
    else:
        buscar = ''
        resultado={}

    context['resultado'] = resultado

    return render(request, template_name, context)

def MapasDetalleView(request, slug):
    template_name = 'generales/mapas_detalle.html'
    hoy = date.today()
    mapas1 = MapasDetalle.objects.filter(slug=slug).last()
    mapas = Mapas.objects.all().order_by('tema')
    categorias = Categoria.objects.all().order_by('id')
    subcategorias = SubCategoria.objects.all().order_by('id')
    context = {'hoy': hoy, 'mapas': mapas, 'mapas1': mapas1, 'categorias': categorias, 'subcategorias': subcategorias}
    if request.POST.get('buscar'):
        buscar = (request.POST.get('buscar').upper())
        template_name="generales/search.html"
        try:
            resultado = Noticias.objects.filter(titulo__icontains=buscar).order_by('-id')
            #paginator5 = Paginator(resultado, 10)
        except:
            resultado = Noticias.objects.filter(titulo__icontains=buscar).order_by('-id')
            #paginator5 = Paginator(resultado, 10)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        #try:
        #    resultado = paginator5.page(page)
        #except (EmptyPage, InvalidPage):
        #    resultado = paginator5.page(paginator5.num_pages)

        #context['paginator5'] = paginator5
        context['resultado'] = resultado
    else:
        buscar = ''
        resultado={}
    form_comentario = ComentarioForm()

    if request.POST.get('email'):
        form_home = SuscribirseForm(request.POST)
        if form_home.is_valid():
            post = form_home.save(commit=False)
            post.save()
            success_url=reverse_lazy("/")

            return JsonResponse(
                {
                    'content': {
                        'message': 'Gracias por suscribirse.',
                    }
                }
            )
        else:
            return JsonResponse(
                {
                    'content': {
                        'message': 'Ya ha sido registrado. Gracias!',
                    }
                }
            )
    else:
        form_home = SuscribirseForm()

    context['form_home'] = form_home
    context['form_comentario'] = form_comentario
    context['regresivo'] = {'activo': False}

    return render(request, template_name, context)

def VerMapaView(request, slug):
    template_name = 'generales/vermapa.html'
    hoy = date.today()
    mapas1 = MapasDetalle.objects.filter(slug=slug).last()
    mapas = Mapas.objects.all().order_by('tema')
    categorias = Categoria.objects.all().order_by('id')
    subcategorias = SubCategoria.objects.all().order_by('id')
    context = {'hoy': hoy, 'mapas': mapas, 'mapas1': mapas1, 'categorias': categorias, 'subcategorias': subcategorias}
    return render(request, template_name, context)

def DetalleView(request, slug):
    template_name = 'generales/detalle.html'
    hoy = date.today()
    detalle = Noticias.objects.filter(slug=slug).last()
    cat = detalle.subcategoria.categoria.id
    scat = detalle.subcategoria.id
    categorias = Categoria.objects.all().order_by('id')
    subcategorias = SubCategoria.objects.all().order_by('id')
    seccion = Categoria.objects.get(id=cat)
    noticias = Noticias.objects.filter(subcategoria__id=scat).exclude(slug=slug).order_by('-fecha')[:10]
    context = {'hoy': hoy, 'noticias': noticias, 'categorias_mul': Categoria_multimedia.objects.all(), 'categorias': categorias, 'subcategorias': subcategorias, 'seccion': seccion, 'detalle':detalle, 'cat': cat, 'modulos': SubCategoria.objects.filter(categoria__id=20).order_by('id')}

    if request.POST.get('buscar'):
        buscar = (request.POST.get('buscar').upper())
        template_name="generales/search.html"
        try:
            resultado = Noticias.objects.filter(titulo__icontains=buscar).order_by('-id')
            #paginator5 = Paginator(resultado, 10)
        except:
            resultado = Noticias.objects.filter(titulo__icontains=buscar).order_by('-id')
            #paginator5 = Paginator(resultado, 10)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        #try:
        #    resultado = paginator5.page(page)
        #except (EmptyPage, InvalidPage):
        #    resultado = paginator5.page(paginator5.num_pages)

        #context['paginator5'] = paginator5
        context['resultado'] = resultado
    else:
        buscar = ''
        resultado={}

    #if request.method == "POST":
    if request.POST.get('comentario'):
        form_comentario = ComentarioForm(request.POST)
        if form_comentario.is_valid():
            post = form_comentario.save(commit=False)
            post.noticia = detalle
            post.save()

            return JsonResponse(
                {
                    'content': {
                        'message': 'Gracias por su comentario.',
                    }
                }
            )
    else:
        form_comentario = ComentarioForm()

    if request.POST.get('email'):
        form_home = SuscribirseForm(request.POST)
        if form_home.is_valid():
            post = form_home.save(commit=False)
            post.save()
            success_url=reverse_lazy("/")

            return JsonResponse(
                {
                    'content': {
                        'message': 'Gracias por suscribirse.',
                    }
                }
            )
        else:
            return JsonResponse(
                {
                    'content': {
                        'message': 'Ya ha sido registrado. Gracias!',
                    }
                }
            )
    else:
        form_home = SuscribirseForm()

    context['form_home'] = form_home
    context['form_comentario'] = form_comentario
    context['regresivo'] = {'activo': False}

    return render(request, template_name, context)

def DetalleImgView(request, pk, tarea):
    template_name = 'generales/detalle_img.html'
    hoy = date.today()
    if tarea == 1:
        detalle = Imagenes.objects.filter(id=pk).last()
    else:
        detalle = Videos.objects.filter(id=pk).last()
    categorias = Categoria.objects.all().order_by('id')
    subcategorias = SubCategoria.objects.all().order_by('id')
    noticias = Noticias.objects.all().order_by('-fecha')[:10]
    context = {'hoy': hoy, 'noticias': noticias, 'tarea': tarea, 'categorias_mul': Categoria_multimedia.objects.all(), 'categorias': categorias, 'subcategorias': subcategorias, 'detalle':detalle, 'modulos': SubCategoria.objects.filter(categoria__id=20).order_by('id')}

    if request.POST.get('buscar'):
        buscar = (request.POST.get('buscar').upper())
        template_name="generales/search.html"
        try:
            resultado = Noticias.objects.filter(titulo__icontains=buscar).order_by('-id')
            #paginator5 = Paginator(resultado, 10)
        except:
            resultado = Noticias.objects.filter(titulo__icontains=buscar).order_by('-id')
            #paginator5 = Paginator(resultado, 10)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        #try:
        #    resultado = paginator5.page(page)
        #except (EmptyPage, InvalidPage):
        #    resultado = paginator5.page(paginator5.num_pages)

        #context['paginator5'] = paginator5
        context['resultado'] = resultado
    else:
        buscar = ''
        resultado={}

    #if request.method == "POST":
    if request.POST.get('comentario'):
        form_comentario = ComentarioForm(request.POST)
        if form_comentario.is_valid():
            post = form_comentario.save(commit=False)
            post.noticia = detalle
            post.save()

            return JsonResponse(
                {
                    'content': {
                        'message': 'Gracias por su comentario.',
                    }
                }
            )
    else:
        form_comentario = ComentarioForm()

    if request.POST.get('email'):
        form_home = SuscribirseForm(request.POST)
        if form_home.is_valid():
            post = form_home.save(commit=False)
            post.save()
            success_url=reverse_lazy("/")

            return JsonResponse(
                {
                    'content': {
                        'message': 'Gracias por suscribirse.',
                    }
                }
            )
        else:
            return JsonResponse(
                {
                    'content': {
                        'message': 'Ya ha sido registrado. Gracias!',
                    }
                }
            )
    else:
        form_home = SuscribirseForm()

    context['form_home'] = form_home
    context['form_comentario'] = form_comentario
    context['regresivo'] = {'activo': False}

    return render(request, template_name, context)

class SinPrivilegios(PermissionRequiredMixin):
    login_url = 'generales:sin_privilegios'
    raise_exception = False
    redirect_field_name = "redirecto_to"

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy(self.login_url))

class HomePage(generic.View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Pagina de Inicio')

class HomeSinPrivilegios(generic.TemplateView):
    template_name = "generales/msg_sin_privilegios.html"

class VideoLiveView(generic.TemplateView):
    template_name = "generales/video_en_vivo.html"

    def get(self, request, *args, **kwargs):
        pauta = Pauta.objects.filter(videolive=True)
        results = resul_votacio.objects.all().order_by('-votos')
        for i, item in enumerate(pauta):
            if item.html.strip() != '':
                html = item.html
        return self.render_to_response(
            self.get_context_data(
                hoy = date.today(),
                results = results,
                html = html
            )
        )

def ajax_update(request, *args, **kwargs):
    results = resul_votacio.objects.all().order_by('-votos')
    return render(request, "generales/tbl_results.html", {'results': results})

class ContactView(generic.CreateView):
    model = Contacto
    template_name = 'generales/contact.html'
    form_class = ContactoForm
    success_url = reverse_lazy("generales:home")

    def get(self, request, *args, **kwargs):
        titulares1 = Noticias.objects.filter(orden=0, subcategoria__id=1).exclude(subcategoria=12).order_by('-id')[:2]
        categorias = Categoria.objects.all().order_by("nombre")
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        return self.render_to_response(
            self.get_context_data(
                form=form,
                titulares1=titulares1,
                categorias=Categoria.objects.all().order_by('id'),
                subcategorias=SubCategoria.objects.all().order_by('id'),
                categorias_mul=Categoria_multimedia.objects.all(),
                modulos=SubCategoria.objects.filter(categoria__id=20).order_by('id'),
                nosotros=Nosotros.objects.all().last(),
                hoy = date.today()
            )
        )

def create_wfs(url):
    """
    Function that connect to GeoServer and return a WFS/OWS service
    
    Args:
        url: A string -> str
    
    Return:
        A WFS/OWS service -> owslib.feature.wfs110.WebFeatureService_1_1_0 object
    """
    return WebFeatureService(url, version='2.0.0')

def get_data(wfs, layer):
    """
    Function that returns a GeoDataFrame or GeoJSON of data layer
    
    Args:
        wfs: A WFS/OWS service -> owslib.feature.wfs110.WebFeatureService_1_1_0 object
        layer: A layer name -> str
    
    Return:
        A GeoDataFrame or GeoJSON data layer -> DataFrame or Dict
    

    # Fetch data from WFS
    r = wfs.getfeature(typename=layer, outputFormat='json')
    
    # Get geometry layer
    json_ = json.loads(r.read())
    geom = json_['features'][0]['geometry']['type']

    if geom == 'Point':
        # Get GeoDataFrame layer
        data = get_gdf(layer)
    else:
        data = json_
        
    return data, geom

    """
    # Define parameters
    service = 'WFS'
    version = '2.0.0'
    request = 'GetFeature'
    outputFormat = 'json'

    # Specify parameters (read data in json format).
    params = dict(service=service,
                  version=version,
                  request=request,
                  typeName=layer,
                  outputFormat=outputFormat)

    # Fetch geojson data from WFS using requests
    r = requests.get(wfs, params=params)

    # Fetch data from WFS
    #r = wfs.getfeature(typename=layer, outputFormat='json')
    
   # Get geometry layer
    json_ = json.loads(r.content)
    geom = json_['features'][0]['geometry']['type']
        
    return json_, geom

def get_gdf(layer):
    # Define parameters
    service = 'WFS'
    version = '2.0.0'
    request = 'GetFeature'
    outputFormat = 'json'
    wfs_url = 'https://smt-test.onic.org.co/geoserver/wfs?'

    # Specify parameters (read data in json format).
    params = dict(service=service,
                  version=version,
                  request=request,
                  typeName=layer,
                  outputFormat=outputFormat)

    # Fetch data from WFS using requests
    r = requests.get(wfs_url, params=params)

    # Create GeoDataFrame from geojson
    gdf = gpd.GeoDataFrame.from_features(geojson.loads(r.content))

    # Define crs
    gdf.crs = CRS.from_epsg(4686)
    return gdf

async def get_point_map(gjson, gdf, name_layer, catalogo):
    # Create a map instance
    mymap = folium.Map(
        location=[4.668730, -72.100403],
        zoom_start=12,
        tiles='cartodbpositron',
        #attributionControl = False,
        prefer_canvas=True)
    fields = list(gjson['features'][0]['properties'].keys())
    names = ""
    vakues_list = []
    for field in fields:
        names += '<b>' + field + '</b>' + ':{}<br>'
        innerlist = gdf[field].values.tolist()
        vakues_list.append(innerlist)
    lat = gdf["geometry"].apply(lambda geom: geom.x)
    lon = gdf["geometry"].apply(lambda geom: geom.y)
    marker_cluster = MarkerCluster(
        name=name_layer,
        overlay=True,
        control=False,
        icon_create_function=None
    )
    for k in range(len(lon)):
        values = [item[k] for item in vakues_list]
        location = lon[k], lat[k]
        marker = folium.Marker(location=location)
        popup = names.format(*values)
        folium.Popup(popup).add_to(marker)
        marker_cluster.add_child(marker)
    marker_cluster.add_to(mymap)
    mapdata = folium.GeoJson(
        gjson,
        name = name_layer,
        zoom_on_click=True,
        show=False
    ).add_to(mymap)
    layers = catalogo
    idx_layer = layers.index(name_layer)
    if idx_layer == 0:
        search_field = fields[2]  
    elif idx_layer == 1:
        search_field = fields[3]
    elif idx_layer == 2:
        search_field = fields[5]
    elif idx_layer == 3:
        search_field = fields[7]    
    else: 
        search_field = fields[0]
    controlsearch = Search(
        layer=mapdata,
        geom_type='Point',
        placeholder='Buscador capa ' + name_layer,
        cllapsed=False,
        search_label=search_field,    
    ).add_to(mymap)  
    folium.LayerControl().add_to(mymap)

    return mymap

def get_polygon_map(gjson, name_layer, catalogo):
    mymap = folium.Map(
        location=[4.668730, -72.100403],
        zoom_start=6,
        titles='cartodbpositron', attributionControl = False,
        prefer_canvas=True)
    names = list(gjson['features'][0]['properties'].keys())    
    popup = folium.GeoJsonPopup(
        fields=names,
        localize=True,
        labels=True,
    )
    mapdata = folium.GeoJson(
        gjson,
        name = name_layer,
        popup=popup,
        highlight_function=lambda x: {"fillOpacity": 0.8},
        zoom_on_click=True,
    ).add_to(mymap)
    layers = catalogo
    idx_layer = layers.index(name_layer)
    if idx_layer == 0:
        search_field = names[2]  
    elif idx_layer == 1:
        search_field = names[3]
    elif idx_layer == 2:
        search_field = names[5]
    elif idx_layer == 3:
        search_field = names[7]    
    else: 
        search_field = names[0]
    controlsearch = Search(
        layer=mapdata,
        geom_type='Polygon',
        placeholder='Buscador capa ' + name_layer,
        cllapsed=False,
        search_label=search_field,    
    ).add_to(mymap)
    folium.LayerControl().add_to(mymap)

    return mymap

def format_iter(iterable, fmt='{!r}', sep=', '):
    return sep.join(fmt.format(x) for x in iterable)

class ajax_updateCapas(generic.View):
    
    def get(self, request):
        capa = int(request.GET.get('capa', 0))
        layer_name = request.GET.get('nombre', '')
        wfs_url = 'https://smt-test.onic.org.co/geoserver/wfs?'

        # Get data and geometry type layer
        gjson_data = get_data(wfs_url, layer_name)
        geom_type = gjson_data['features'][0]['geometry']['type']

        #capas
        wfs = create_wfs(wfs_url)
        layers_catalogue = wfs.contents
        catalogo=[]
        for i, item in enumerate(layers_catalogue):
            catalogo.append(item)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        if geom_type == 'Point':
            gdf = gpd.GeoDataFrame.from_features(gjson_data)
            gdf.crs = CRS.from_epsg(4686)
            my_map = loop.run_until_complete(get_point_map(gjson_data, gdf, layer_name, catalogo))
        else:
            my_map = loop.run_until_complete(get_polygon_map(gjson_data, layer_name, catalogo))

        map = my_map._repr_html_()

        return JsonResponse(
            {
                'content': {
                    'mapa': map
                }
            }
        )
    
class Visor(LoginRequiredMixin, generic.TemplateView):
    template_name='visor/visor.html'
    login_url='generales:login'

    def get(self, request, *args, **kwargs):
        categorias = Categoria.objects.all().order_by('id')
        subcategorias = SubCategoria.objects.all().order_by('id')
        lat = 4.668730
        lon = -72.100403
        logo_path = "static/base/image/favicon.png"
        m = folium.Map(location=[lat, lon], zoom_start=5, attributionControl = False)     
        m = m._repr_html_()
        wfs_url = 'https://smt-test.onic.org.co/geoserver/wfs?'
        wfs = create_wfs(wfs_url)
        layers_catalogue = wfs.contents
        catalogo=[]
        for i, item in enumerate(layers_catalogue):
            catalogo.append(item.replace('geonode:', '')) #[8:]
        context = super().get_context_data(**kwargs)
        context = {'mapa': m, 'l': len(layers_catalogue)}
        
        return self.render_to_response( 
            self.get_context_data(
                context=context,
                mapa=m,
                catalogo=catalogo,
                subcategorias = subcategorias,
                categorias = categorias,
                categorias_mul = Categoria_multimedia.objects.all(),
                modulos = SubCategoria.objects.filter(categoria__id=20).order_by('id')
            )
        )