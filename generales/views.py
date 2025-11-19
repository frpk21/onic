from datetime import date
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from generales.choices import OrderNews
from generales.forms import SuscribirseForm, ComentarioForm, ContactoForm, CodeVerificationForm
from generales.models import Noticias, Contacto, VideoSMT, Nosotros, Categoria, Mapas, MapasDetalle, Equipo, Podcast, \
    Videos, Imagenes, Categoria_multimedia, Project
from django.core.cache import cache
from generales.models import Categoria
from datetime import date
from django.http import JsonResponse
from django.db.models import Prefetch
from generales.models import Noticias, VideoSMT, Nosotros, OrderNews
from generales.forms import SuscribirseForm
from datetime import date
from django.http import JsonResponse
from django.db.models import Prefetch
from .models import Noticias, VideoSMT, Nosotros
from .forms import SuscribirseForm
from .choices import OrderNews
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views.generic import FormView, View
from django.urls import reverse
from .forms import RegisterForm
from .models import PendingUser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
import random
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import ActivationCode
from django.core.paginator import Paginator

def categorias_context(request):
    return {
        'MENU_CATEGORIES': Categoria.objects.prefetch_related('subs').all()
    }

def HomeView(request):

    hoy = date.today()
    noticias_qs = Noticias.objects.select_related(
        "autor", "categoria"
    ).only(
        "id", "titulo", "subtitulo", "fecha", "orden",
        "imagen", "slug",
        "categoria__id", "categoria__nombre",
        "autor__id", "autor__username",
    )

    # Titulares
    titulares = noticias_qs.filter(
        orden=OrderNews.NEWS
    ).order_by("-fecha")[:6]
    print(">>>>>>>> TITULARES:", titulares.count()) 
    """
    # Carrusel
    carrusel = noticias_qs.filter(
        orden=OrderNews.CAROUSEL
    ).order_by("-fecha")[:3]
    """
    
    # Ultima noticia destacada
    noticia_destacada = noticias_qs.filter(
        orden=OrderNews.NEWS
    ).order_by("-fecha").first()

    # Último video SMT
    video_smt = VideoSMT.objects.only("titulo", "url_video").last()

    # Contenido de Nosotros
    nosotros = Nosotros.objects.only(
        "descripcion", "vision", "justificacion", "objetivos", "usuarios",
        "imagen", "imagen_vision", "imagen_jus", "imagen_obj", "imagen_users"
    ).last()

    # Novedades (updates)
    novedades = noticias_qs.filter(
        orden=OrderNews.UPDATES
    ).order_by("-fecha")[:7]

    if request.POST.get("buscar"):
        buscar = request.POST.get("buscar").strip()

        resultados = noticias_qs.filter(
            titulo__icontains=buscar
        ).order_by("-id")

        return render(request, "generales/search.html", {
            "resultado": resultados,
            "buscar": buscar,
            "hoy": hoy,
        })

    context = {
        "hoy": hoy,
        "titulares": titulares,
        "noticias": noticia_destacada,
        "video_smt": video_smt,
        "nosotros": nosotros,
        "novedades": novedades,
        "resultado": {},
    }

    return render(request, "generales/home.html", context)



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

    mapas_list = Mapas.objects.filter(activo=True).order_by('tema')

    paginator = Paginator(mapas_list, 8)

    page_number = request.GET.get('page')
    mapas_page = paginator.get_page(page_number)

    context = {
        'mapas': mapas_page,
        'page_obj': mapas_page,
        'paginator': paginator,
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
    publicaciones_qs = MapasDetalle.objects.filter(
        mapa_id=pk, 
        activo=True
    ).order_by('titulo')

    tit_obj = MapasDetalle.objects.filter(
        mapa_id=pk, 
        activo=True
    ).last()
    titulo = tit_obj.titulo if tit_obj else "Publicaciones"
    paginator = Paginator(publicaciones_qs, 8)
    page_number = request.GET.get('page')
    publicaciones = paginator.get_page(page_number)

    context = {
        'tit': titulo,
        'pk': pk,
        'publicaciones': publicaciones,
        'paginator': paginator
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
    else:
        buscar = ''
        resultado={}

    context['resultado'] = resultado

    return render(request, template_name, context)

def MapasDetalleView(request, slug):
    template_name = 'generales/mapas_detalle.html'

    # Obtener el mapa por su slug
    mapa_detalle = MapasDetalle.objects.filter(slug=slug, activo=True).last()

    if not mapa_detalle:
        return render(request, template_name, {'error': 'El mapa no existe'})

    # Obtener todos los mapas (para menú, sidebar o filtros)
    mapas = Mapas.objects.all().order_by('tema')

    # Publicaciones relacionadas del mismo mapa
    publicaciones_relacionadas = MapasDetalle.objects.filter(
        mapa_id=mapa_detalle.mapa_id,
        activo=True
    ).exclude(id=mapa_detalle.id).order_by('titulo')

    context = {
        'mapas': mapas,
        'mapa_detalle': mapa_detalle,
        'publicaciones_relacionadas': publicaciones_relacionadas,
    }

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
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.exclude(id=self.object.id).order_by('-modificado')[:4]
        context['latest_news'] = Noticias.objects.order_by('-fecha')[:5]

        return context

class ProjectListView(generic.ListView):
    model = Project
    paginate_by = 5
    
    def get_queryset(self):
        qs = Project.objects.filter(activo=True).order_by('-modificado')
        for p in qs:
            if p.meta and p.meta > 0:
                p.porcentaje = round((p.donado / p.meta) * 100, 2)
            else:
                p.porcentaje = 0
        category_id = self.request.GET.get('category')
        if category_id:
            qs = qs.filter(category_id=category_id)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['is_iphone'] = 'iphone' in str(
            self.request.META.get('HTTP_USER_AGENT', '')
        ).lower()
        category_id = self.request.GET.get('category')
        ctx['category'] = Categoria.objects.filter(id=category_id).first()
        ctx['latest_news'] = Noticias.objects.order_by('-fecha')[:5]

        return ctx

class PolicyView(generic.TemplateView):
    template_name = 'generales/policy.html'
    success_url = reverse_lazy("generales:home")

@require_POST
def verificar_codigo(request):

    user_id = request.POST.get("user_id")
    code = request.POST.get("code", "").strip()

    # Validar datos vacíos
    if not user_id or not code:
        return JsonResponse({
            "status": "error",
            "message": "Datos incompletos, por favor inténtalo nuevamente."
        })

    # Validar usuario
    user = get_object_or_404(User, pk=user_id)

    # Validar código de activación
    try:
        activation = ActivationCode.objects.get(user=user)
    except ActivationCode.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "No existe un código válido para tu cuenta."
        })

    # Comparar código
    if activation.code == code:
        user.is_active = True
        user.save()
        activation.delete()

        return JsonResponse({
            "status": "ok",
            "message": "✔ Cuenta activada correctamente"
        })

    return JsonResponse({
        "status": "error",
        "message": "❌ Código incorrecto, intenta nuevamente."
    })

class RegisterView(FormView):
    template_name = "generales/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("generales:register")

    def form_valid(self, form):
        # NO volver a validar form.is_valid() !!
        user = form.save()
        user.is_active = False
        user.save()

        # Generar código
        code = str(random.randint(100000, 999999))
        ActivationCode.objects.update_or_create(
            user=user,
            defaults={"code": code}
        )

        # Enviar correo
        send_mail(
            "Código de activación",
            f"Tu código de activación es: {code}",
            "administrador@sistemainrai.net",
            [user.email],
            fail_silently=True,
        )

        # Mostrar modal de verificación
        return render(self.request, "generales/register.html", {
            "form": RegisterForm(),
            "user_id": user.id,
            "show_modal": True,
        })

    def form_invalid(self, form):
        # Renderizar la MISMA plantilla, mostrando errores
        return render(self.request, "generales/register.html", {
            "form": form,
            "show_modal": False,  # NO se abre el modal si hay errores
        })


def activate_account(request):
    if request.method == "POST":
        code = request.POST.get("code")
        user_id = request.POST.get("user_id")

        try:
            user = User.objects.get(id=user_id)
            activation = ActivationCode.objects.get(user=user)

            if activation.code == code:
                user.is_active = True
                user.save()
                activation.delete()
                return JsonResponse({"status": "ok"})
            else:
                return JsonResponse({"status": "error", "message": "Código incorrecto"})
        except:
            return JsonResponse({"status": "error", "message": "Usuario o código inválido"})

    return JsonResponse({"status": "error"})
