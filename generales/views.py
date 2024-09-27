from datetime import date

from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from generales.choices import OrderNews
from generales.forms import SuscribirseForm, ComentarioForm, ContactoForm
from generales.models import Noticias, Contacto, VideoSMT, Nosotros, Categoria, Mapas, MapasDetalle, Equipo, Podcast, \
    Videos, Imagenes, Categoria_multimedia, Project


def HomeView(request):
    hoy = date.today()
    carrusel = Noticias.objects.filter(orden=OrderNews.CAROUSEL).order_by('-fecha')[:3]
    noticias = Noticias.objects.filter(orden=OrderNews.NEWS).last()
    video_smt = VideoSMT.objects.all().last()
    nosotros = Nosotros.objects.all().last()
    novedades = Noticias.objects.filter(orden=OrderNews.UPDATES).order_by('-fecha')[:7]

    context = {
        'hoy': hoy,
        'carrusel': carrusel,
        'noticias': noticias,
        'video_smt': video_smt,
        'nosotros': nosotros,
        'novedades': novedades,
    }
    if request.POST.get('email'):
        form_home = SuscribirseForm(request.POST)
        if form_home.is_valid():
            post = form_home.save(commit=False)
            post.save()
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
        template_name = "generales/search.html"
        try:
            resultado = Noticias.objects.filter(titulo__icontains=buscar).order_by('-id')
        except:
            resultado = Noticias.objects.filter(titulo__icontains=buscar).order_by('-id')

        context['form_search'] = resultado
    else:
        resultado = {}
        template_name = "generales/home.html"

    context['form_home'] = form_home
    context['resultado'] = resultado

    return render(request, template_name, context)


def SeccionView(request, pk):
    template_name = 'generales/seccion.html'
    seccion = Categoria.objects.get(id=pk)
    sub = Categoria.objects.filter(parent=seccion)
    noticias = Noticias.objects.filter(categoria=seccion).order_by('-fecha')[:20]
    context = {
        'noticias': noticias,
        'seccion': seccion,
    }

    resultado = {}
    if request.POST.get('buscar'):
        template_name = "generales/search.html"
        resultado = Noticias.objects.filter(titulo__icontains=request.POST.get('buscar').upper()).order_by('-id')

    context['resultado'] = resultado

    return render(request, template_name, context)

def NosotrosView(request):
    template_name = 'generales/nosotros.html'
    context = {
        'img_bak': Categoria.objects.get(id=request.GET['category']),
        'nosotros': Nosotros.objects.all().last(),
    }
    return render(request, template_name, context)


def EquipoView(request):
    template_name = 'generales/equipo.html'
    context = {
        'concejero': Equipo.objects.filter(orden=0).last(),
        'nosotros': Nosotros.objects.all().last(),
        'equipo': Equipo.objects.filter(activo=True).exclude(orden=0).order_by('orden'),
    }
    return render(request, template_name, context)


def BoletinesView(request):
    template_name = 'generales/boletines.html'
    context = {
        'img_bak': Categoria.objects.get(pk=request.GET['category']),
        'noticias': Noticias.objects.all().order_by('-fecha')[:10],
        'boletines': Noticias.objects.filter(orden=3).order_by('-fecha'),
        'categorias': Categoria.objects.filter(parent__isnull=True),
    }
    return render(request, template_name, context)

def Mapas0View(request):
    template_name = 'generales/mapas0.html'
    context = {
        'img_bak': Categoria.objects.get(id=request.GET['category']),
        'mapas': Mapas.objects.filter(activo=True).order_by('tema'),
    }
    return render(request, template_name, context)

def PublicacionesView(request, pk):
    template_name = 'generales/public.html'
    categoria = Categoria.objects.get(id=pk)
    context = {
        'tit': '',
        'img_bak': categoria,
        'publicaciones': categoria.noticias_set.all().order_by('-fecha'),
    }
    return render(request, template_name, context)


def MapsGalleryGroupView(request, pk):
    template_name = 'generales/publick_maps.html'
    publicaciones = MapasDetalle.objects.filter(mapa_id=pk, activo=True).order_by('titulo')
    img_bak = Categoria.objects.get(id=request.GET['category'])
    tit = MapasDetalle.objects.filter(mapa_id=pk, activo=True).last()
    context = {
        'tit': tit,
        'img_bak': img_bak,
        'pk': pk,
        'publicaciones': publicaciones,
    }
    return render(request, template_name, context)


def ModulosView(request, pk):
    template_name = 'generales/modulos.html'
    categoria = Categoria.objects.get(id=pk)
    noticias = Noticias.objects.filter(categoria=categoria).last()
    context = {
        'modulos2': Categoria.objects.filter(parent=categoria.parent).order_by('orden'),
        'noticias': noticias,
        'modulo': categoria,
    }
    return render(request, template_name, context)



def MultimediaView(request):
    template_name = 'generales/multimedia.html'
    context = {'categoria': Categoria.objects.get(id=request.GET['category'])}
    return render(request, template_name, context)


def Multimedia2View(request, pk):
    template_name = 'generales/multimedia2.html'
    cat_multimedia = Categoria_multimedia.objects.get(id=pk)
    multimedia = Noticias.objects.filter(categoria_id=request.GET['category']).order_by('-fecha')
    podcast = Podcast.objects.filter(categoria_multimedia=cat_multimedia).order_by('-fecha')
    videos = Videos.objects.filter(categoria_multimedia=cat_multimedia).order_by('-fecha')
    imagenes = Imagenes.objects.filter(categoria_multimedia=cat_multimedia).order_by('-fecha')
    mediateca = Noticias.objects.filter(orden=OrderNews.MEDIA_LIBRARY).order_by('-fecha')[:3]
    context = {
        'mediateca': mediateca,
        'podcast': podcast,
        'videos': videos,
        'imagenes': imagenes,
        'multimedia': multimedia,
        'cat_multimedia': cat_multimedia,
    }

    return render(request, template_name, context)

def SubSeccionView(request, pk):
    template_name = 'generales/seccion.html'
    noticias = Noticias.objects.filter(subcategoria__id=pk).order_by('-fecha')[:20]
    context = {
        'noticias': noticias,
        'seccion': Categoria.objects.get(id=pk),
    }
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
    mapas1 = MapasDetalle.objects.filter(slug=slug).last()
    mapas = Mapas.objects.all().order_by('tema')
    context = {
        'img_bak': Categoria.objects.get(id=request.GET['category']),
        'mapas': mapas,
        'mapas1': mapas1,
    }
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
    context = {
        'img_bak': Categoria.objects.filter(id=request.GET.get('category')).last(),
        'mapas1': MapasDetalle.objects.filter(slug=slug).last(),
    }
    return render(request, template_name, context)


def DetalleView(request, slug):
    template_name = 'generales/detalle.html'
    noticia = Noticias.objects.filter(slug=slug).last()
    noticias = noticia.categoria.noticias_set.exclude(id=noticia.id, slug='').order_by('-fecha')[:10]
    context = {
        'noticias': noticias,
        'seccion': noticia.categoria.parent,
        'detalle': noticia,
    }
    if request.POST.get('buscar'):
        buscar = (request.POST.get('buscar').upper())
        template_name="generales/search.html"
        try:
            resultado = Noticias.objects.filter(titulo__icontains=buscar).order_by('-id')
        except:
            resultado = Noticias.objects.filter(titulo__icontains=buscar).order_by('-id')

        context['resultado'] = resultado

    if request.POST.get('comentario'):
        form_comentario = ComentarioForm(request.POST)
        if form_comentario.is_valid():
            post = form_comentario.save(commit=False)
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
    if tarea == 1:
        detalle = Imagenes.objects.filter(id=pk).last()
    else:
        detalle = Videos.objects.filter(id=pk).last()
    noticias = Noticias.objects.all().order_by('-fecha')[:10]

    context = {
        'noticias': noticias,
        'tarea': tarea,
        'detalle': detalle,
    }

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


# def ajax_update(request, *args, **kwargs):
#     results = resul_votacio.objects.all().order_by('-votos')
#     return render(request, "generales/tbl_results.html", {'results': results})

class ContactView(generic.CreateView):
    model = Contacto
    template_name = 'generales/contact.html'
    form_class = ContactoForm
    success_url = reverse_lazy("generales:home")

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        return self.render_to_response(
            self.get_context_data(form=form)
        )


class ProjectDetailView(generic.DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        kwargs['category'] = Categoria.objects.get(id=self.request.GET['category'])
        context_data = super().get_context_data(**kwargs)
        context_data['projects'] = Project.objects.exclude(id=self.object.id)
        return context_data


class ProjectListView(generic.ListView):
    model = Project
    paginate_by = 20

    def get_context_data(self, *args, object_list=None, **kwargs):
        kwargs['category'] = Categoria.objects.get(id=self.request.GET['category'])
        return super().get_context_data(*args, object_list=object_list, **kwargs)
