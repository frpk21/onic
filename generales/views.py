from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse_lazy

from django.views import generic

from django.contrib.auth.mixins import PermissionRequiredMixin

from generales.models import Noticias, Comentario, Contacto, VideoSMT, Nosotros, Categoria, SubCategoria

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
    boletines = Noticias.objects.filter(orden=3).order_by('-id')[:7]
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
        'categorias' : Categoria.objects.all(),
        'subcategorias': SubCategoria.objects.all()
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
    categorias = Categoria.objects.all()
    subcategorias = SubCategoria.objects.all()
    seccion = Categoria.objects.get(id=pk)
    noticias = Noticias.objects.filter(subcategoria__categoria__id=pk).order_by('-id', 'subcategoria__id','orden')[:20]
    context = {'hoy': hoy, 'noticias': noticias, 'categorias': categorias, 'subcategorias': subcategorias, 'seccion': seccion}

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


def SubSeccionView(request, pk):
    template_name = 'generales/seccion.html'
    hoy = date.today()
    categorias = Categoria.objects.all().order_by("nombre")
    subcategorias = SubCategoria.objects.all().order_by("nombre")
    seccion = SubCategoria.objects.get(id=pk)
    noticias = Noticias.objects.filter(subcategoria__categoria__id=pk).order_by('-id', 'subcategoria__id','orden')[:20]
    context = {'hoy': hoy, 'noticias': noticias, 'categorias': categorias, 'subcategorias': subcategorias, 'seccion': seccion}
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
    vista = Noticias.objects.filter(slug=slug).last()
    vista = vista.vistas + 1
    Noticias.objects.filter(slug=slug).update(vistas=vista)
    hoy = date.today()
    detalle0 = Noticias.objects.filter(slug=slug)
    for i, item in enumerate(detalle0):
        cat = item.subcategoria
        detalle = item
        pk = item.id
    try:
        pauta_detalle1 = Pauta.objects.filter(fecha_inicio_publicacion__lte=hoy, fecha_final_publicacion__gte=hoy, orden=9).last()
    except:
        pauta_detalle1 = {}
    titulares1 = Noticias.objects.filter(orden=0, subcategoria__id=1).exclude(subcategoria=12).order_by('-id')[:4]
    titulares2 = Noticias.objects.filter(orden=0, subcategoria__id=2).order_by('-id')[:4]
    titulares3 = Noticias.objects.filter(orden=0, subcategoria__categoria__gte=2).order_by('-id')[:4]
    virales = Noticias.objects.filter(viral=True, ultima_hora=False ).order_by('-id')[:5]
    ultima_hora = Noticias.objects.filter(ultima_hora=True).order_by('-id')[:3]
    loquepasa = Noticias.objects.filter(viral=False, ultima_hora=False, subcategoria__categoria=1, orden__gt=0).exclude(fecha_inicio_publicacion__gte=hoy).order_by('-id')[:8]
    loquesuena = Noticias.objects.filter(viral=False, ultima_hora=False, subcategoria__categoria=2, orden__gt=0).exclude(fecha_inicio_publicacion__gte=hoy).order_by('-id')[:8]
    loquesemueve = Noticias.objects.filter(viral=False, ultima_hora=False, subcategoria__categoria=3, orden__gt=0).exclude(fecha_inicio_publicacion__gte=hoy).order_by('-id')[:8]
    sonajero = Noticias.objects.filter(viral=False, ultima_hora=False, subcategoria__categoria=4).order_by('-id')[:8]
    recientes = Noticias.objects.filter(viral=False, ultima_hora=False).exclude(subcategoria=12, id=pk).order_by('-id')[:4]
    populares = Noticias.objects.filter(viral=True, ultima_hora=False).order_by('-vistas')[:4]
    tecno1 = Noticias.objects.filter(orden=0, subcategoria=12, ultima_hora=False).order_by('-id')[:6]
    #tecno2 = Noticias.objects.filter(subcategoria=12).exclude(orden=0, ultima_hora=False).order_by('-id')[:6]
    tecno2 = Noticias.objects.filter(subcategoria=12).order_by('-id')[:6]
    comentarios = Comentario.objects.filter(noticia=pk)
    noticias = Noticias.objects.filter(subcategoria=cat, ultima_hora=False ).exclude(id=pk).order_by('-id')[:3]
    categorias = Categoria.objects.all().order_by("nombre")
    lomasvisto = Noticias.objects.filter(ultima_hora=False, ).order_by('-vistas')[:2]
    subcategorias = SubCategoria.objects.all().order_by("nombre")
    loultimo = Noticias.objects.filter(ultima_hora=False, ).exclude(id=pk).order_by('-id')[:3]
    deportes = Noticias.objects.filter(subcategoria__categoria=1, ultima_hora=False).exclude(id=pk).order_by('-id')[:3]
    fotos = Fotos_destacadas.objects.all().order_by('-id')[:6]

    context = {'hoy': hoy,
            'pauta_detalle1': pauta_detalle1,
            'titulares1': titulares1,
            'titulares2': titulares2,
            'titulares3': titulares3,
            'fotos': fotos,
            'lomasvisto': lomasvisto,
            'ultima_hora': ultima_hora,
            'loquepasa': loquepasa,
            'loquesuena': loquesuena,
            'loquesemueve': loquesemueve,
            'sonajero': sonajero,
            'recientes': recientes,
            'populares': populares,
            'tecno1': tecno1,
            'tecno2': tecno2,
            'noticias': noticias,
            'categorias': categorias,
            'cat':cat,
            'subcategorias': subcategorias,
            'detalle': detalle,
            'loultimo': loultimo,
            'virales': virales,
            'deportes': deportes,
            'comentarios': comentarios}

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

