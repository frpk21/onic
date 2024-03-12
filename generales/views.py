from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse_lazy

from django.views import generic

from django.contrib.auth.mixins import PermissionRequiredMixin

from generales.models import Noticias, Comentario, Contacto, VideoSMT, Nosotros, Categoria, SubCategoria, Equipo

from datetime import date

from django.shortcuts import render

from generales.forms import SuscribirseForm, ComentarioForm, ContactoForm

from django.http import JsonResponse
from datetime import timedelta



def HomeView(request):
    #CHOICES = ((0,'Carrusel'),(1,'Noticia 1'),(2,'Novedades 2'),(3,'Boletines 3'),(4,'Mediateca 4'))
    hoy = date.today()
    carrusel = Noticias.objects.filter(orden=0).order_by('-id')[:3]
    noticias = Noticias.objects.filter(orden=1).last()
    video_smt = VideoSMT.objects.all().last()
    nosotros = Nosotros.objects.all().last()
    novedades = Noticias.objects.filter(orden=2).order_by('-id')[:5]
    boletines = Noticias.objects.filter(orden=3).order_by('-id')[:10]
    mediateca = Noticias.objects.filter(orden=4).order_by('-id')[:3]
    context = {
        'hoy': hoy,
        'carrusel': carrusel,
        'noticias': noticias,
        'video_smt': video_smt,
        'nosotros': nosotros,
        'novedades': novedades,
        'boletines': boletines,
        'mediateca': mediateca,
        'categorias' : Categoria.objects.all().order_by('id'),
        'subcategorias': SubCategoria.objects.all().order_by('id'),
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
    noticias = Noticias.objects.filter(subcategoria__categoria__id=pk).order_by('-id', 'subcategoria__id','orden')[:20]
    context = {'hoy': hoy, 'noticias': noticias, 'categorias': categorias, 'subcategorias': subcategorias, 'seccion': seccion, 'sub': sub, 'modulos': SubCategoria.objects.filter(categoria__id=20).order_by('id')}

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
    context = {'hoy': hoy, 'nosotros': nosotros, 'categorias': categorias, 'subcategorias': subcategorias, 'modulos': SubCategoria.objects.filter(categoria__id=20).order_by('id')}

    return render(request, template_name, context)

def EquipoView(request):
    template_name = 'generales/equipo.html'
    hoy = date.today()
    categorias = Categoria.objects.all().order_by('id')
    subcategorias = SubCategoria.objects.all().order_by('id')
    equipo = Equipo.objects.all().order_by('nombre')
    context = {'hoy': hoy, 'nosotros': Nosotros.objects.all().last(), 'equipo': equipo, 'categorias': categorias, 'subcategorias': subcategorias, 'modulos': SubCategoria.objects.filter(categoria__id=20).order_by('id')}

    return render(request, template_name, context)

def PublicacionesView(request, pk):
    template_name = 'generales/public.html'
    hoy = date.today()
    categorias = Categoria.objects.all().order_by('id')
    subcategoria = SubCategoria.objects.get(id=pk)
    subcategorias = SubCategoria.objects.all().order_by('id')
    publicaciones = Noticias.objects.filter(subcategoria__id=pk)
    c_p = Categoria.objects.get(id=14)  # 14 = Publicaciones
    context = {'hoy': hoy, 'subcategorias': subcategorias, 'cat_p': c_p, 'nosotros': Nosotros.objects.all().last(), 'publicaciones': publicaciones, 'categorias': categorias, 'subcategoria': subcategoria, 'modulos': SubCategoria.objects.filter(categoria__id=20).order_by('id')}

    return render(request, template_name, context)

def ModulosView(request, pk):
    template_name = 'generales/modulos.html'
    hoy = date.today()
    categorias = Categoria.objects.all().order_by('id')
    subcategorias = SubCategoria.objects.all().order_by('id')
    modulo = SubCategoria.objects.get(id=pk)
    modulos2 = SubCategoria.objects.filter(categoria__id=20)   # 20=modulos
    noticias = Noticias.objects.filter(subcategoria__id=pk).last()
    c_p = Categoria.objects.get(id=20)  # 20 = modulos
    context = {'hoy': hoy, 'modulos2': modulos2, 'subcategorias': subcategorias, 'cat_p': c_p, 'nosotros': Nosotros.objects.all().last(), 'noticias': noticias, 'categorias': categorias, 'modulo': modulo, 'modulos': SubCategoria.objects.filter(categoria__id=20).order_by('id')}

    return render(request, template_name, context)

def MultimediaView(request):
    template_name = 'generales/multimedia.html'
    hoy = date.today()
    categorias = Categoria.objects.all().order_by('id')
    subcategoria = SubCategoria.objects.get(id=16)
    subcategorias = SubCategoria.objects.all().order_by('id')
    multimedia = Noticias.objects.filter(subcategoria__id=16)
    c_p = Categoria.objects.get(id=14)  # 14 = Publicaciones
    context = {'hoy': hoy, 'subcategorias': subcategorias, 'cat_p': c_p, 'nosotros': Nosotros.objects.all().last(), 'multimedia': multimedia, 'categorias': categorias, 'subcategoria': subcategoria, 'modulos': SubCategoria.objects.filter(categoria__id=20).order_by('id')}

    return render(request, template_name, context)

def SubSeccionView(request, pk):
    template_name = 'generales/seccion.html'
    hoy = date.today()
    categorias = Categoria.objects.all().order_by('id')
    subcategorias = SubCategoria.objects.all().order_by('id')
    seccion = SubCategoria.objects.get(id=pk)
    noticias = Noticias.objects.filter(subcategoria__id=pk).order_by('-id')[:20]
    context = {'hoy': hoy, 'noticias': noticias, 'categorias': categorias, 'subcategorias': subcategorias, 'seccion': seccion, 'modulos': SubCategoria.objects.filter(categoria__id=20).order_by('id')}
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


def DetalleView(request, slug):
    template_name = 'generales/detalle.html'
    hoy = date.today()
    detalle = Noticias.objects.filter(slug=slug)
    cat, scat = 0, 0
    for i, item in enumerate(detalle):
        cat = item.subcategoria.categoria.id
        scat = item.subcategoria.id
    categorias = Categoria.objects.all().order_by('id')
    subcategorias = SubCategoria.objects.all().order_by('id')
    seccion = Categoria.objects.get(id=cat)
    noticias = Noticias.objects.filter(subcategoria__id=scat).order_by('-id')[:10]
    context = {'hoy': hoy, 'noticias': noticias, 'categorias': categorias, 'subcategorias': subcategorias, 'seccion': seccion, 'detalle':detalle, 'cat': cat, 'modulos': SubCategoria.objects.filter(categoria__id=20).order_by('id')}

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
                hoy = date.today(),
                categorias=categorias
            )
        )

