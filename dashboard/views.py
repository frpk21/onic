from rest_framework.views import APIView
from rest_framework.response import Response
from dashboard.stats_utils import (
    get_dataframe, piramide_poblacional, dependencia, indice_myers
)
from dashboard.models import ChiaDataset
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, Count
from rest_framework.views import APIView
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, String
from reportlab.lib.colors import Color, black, HexColor
from django.http import Http404
import qrcode
from io import BytesIO
import datetime

class DashboardSummary(APIView):
    def get(self, request):

        total = ChiaDataset.objects.count()
        mujeres = ChiaDataset.objects.filter(
            Q(sexo__iexact="F") | 
            Q(sexo__icontains="fem")
        ).count()

        hombres = ChiaDataset.objects.filter(
            Q(sexo__iexact="M") |
            Q(sexo__icontains="mas")
        ).count()

        # Cálculo Myers (si ya lo tienes hecho)
        myers = round(abs((mujeres - hombres) / (total or 1)) * 10, 2)

        return Response({
            "total": total,
            "hombres": hombres,
            "mujeres": mujeres,
            "myers": myers
        })


class PiramideAPIView(APIView):
    def get(self, request):
        df = get_dataframe()
        pir = piramide_poblacional(df)
        return Response(pir.to_dict(orient="records"))


def dashboard_page(request):
    return render(request, "dashboard/dashboard.html")

class SectorPoblacionAPIView(APIView):
    def get(self, request):
        sectores = (
            ChiaDataset.objects
            .values("sector_cnmbr")
            .annotate(
                total=Count("id"),
                mujeres=Count(
                    "id",
                    filter=Q(sexo__iexact="F") | Q(sexo__icontains="fem")
                ),
                hombres=Count(
                    "id",
                    filter=Q(sexo__iexact="M") | Q(sexo__icontains="mas")
                )
            )
            .order_by("sector_cnmbr")
        )

        # Convertir None a "SIN SECTOR" para limpieza
        data = []
        for s in sectores:
            data.append({
                "sector": s["sector_cnmbr"] if s["sector_cnmbr"] else "Sin sector",
                "total": s["total"],
                "hombres": s["hombres"],
                "mujeres": s["mujeres"],
            })

        return Response(data)
    
class EdadResumenAPIView(APIView):
    def get(self, request):
        qs = ChiaDataset.objects.exclude(edad__isnull=True)

        total = qs.count()
        edades = list(qs.values_list("edad", flat=True))

        menores = qs.filter(edad__lt=15).count()
        productiva = qs.filter(edad__gte=15, edad__lt=65).count()
        mayores = qs.filter(edad__gte=65).count()

        dependencia = round(((menores + mayores) / (productiva or 1)), 2)

        return Response({
            "edad_promedio": round(sum(edades) / total, 2),
            "edad_mediana": sorted(edades)[len(edades) // 2],
            "dependencia": dependencia,
            "grupo_0_14": menores,
            "grupo_15_64": productiva,
            "grupo_65_mas": mayores
        })

class EstadoCivilAPIView(APIView):
    def get(self, request):
        qs = (
            ChiaDataset.objects.values("estado_civil")
            .annotate(total=Count("id"))
            .order_by("estado_civil")
        )
        data = [
            {"estado_civil": r["estado_civil"] or "No registrado", "total": r["total"]}
            for r in qs
        ]
        return Response(data)

class EducacionAPIView(APIView):
    def get(self, request):
        qs = (
            ChiaDataset.objects.values("nivel_escol")
            .annotate(total=Count("id"))
            .order_by("nivel_escol")
        )
        data = [
            {"nivel": r["nivel_escol"] or "No registrado", "total": r["total"]}
            for r in qs
        ]
        return Response(data)

class OcupacionAPIView(APIView):
    def get(self, request):
        qs = (
            ChiaDataset.objects.values("ocupacion")
            .annotate(total=Count("id"))
            .order_by("ocupacion")
        )
        data = [
            {"ocupacion": r["ocupacion"] or "No registrado", "total": r["total"]}
            for r in qs
        ]
        return Response(data)

class SaludAPIView(APIView):
    def get(self, request):
        qs = (
            ChiaDataset.objects.values("sis_salud")
            .annotate(total=Count("id"))
            .order_by("sis_salud")
        )
        data = [
            {"regimen": r["sis_salud"] or "No registrado", "total": r["total"]}
            for r in qs
        ]
        return Response(data)

class MigracionAPIView(APIView):
    def get(self, request):
        fuera = ChiaDataset.objects.filter(fuera_resguar="Si").count()
        dentro = ChiaDataset.objects.filter(fuera_resguar="No").count()

        razones = (
            ChiaDataset.objects.values("razon_migra")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        data = {
            "fuera_resguardo": fuera,
            "dentro_resguardo": dentro,
            "razones": [
                {"razon": r["razon_migra"] or "No registrada", "total": r["total"]}
                for r in razones
            ]
        }
        return Response(data)

class ViviendaAPIView(APIView):
    def get(self, request):

        total_hogares = ChiaDataset.objects.values("num_vivien").distinct().count()

        promedio_integrantes = (
            ChiaDataset.objects.aggregate(prom=Count("id") / (total_hogares or 1))["prom"]
        )

        tenencia = (
            ChiaDataset.objects.values("tenencia")
            .annotate(total=Count("id"))
            .order_by("tenencia")
        )

        data = {
            "hogares_totales": total_hogares,
            "prom_integrantes": round(promedio_integrantes, 2),
            "tenencia": [
                {"tipo": r["tenencia"] or "No registrado", "total": r["total"]}
                for r in tenencia
            ]
        }
        return Response(data)

def certificado_buscar(request):
    doc = request.GET.get("doc", "").strip()
    contexto = {}

    if doc:
        existe = ChiaDataset.objects.filter(num_doc__iexact=doc).exists()

        contexto["doc"] = doc
        contexto["existe"] = existe

    return render(request, "dashboard/certificado_buscar.html", contexto)


def certificado_pdf(request, doc):
    persona = ChiaDataset.objects.filter(num_doc=doc).first() or ChiaDataset.objects.filter(num_doc=f"{doc}.0").first()

    if not persona:
        raise Http404("El documento no está registrado en el Censo 2025.")

    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleH = styles["Heading1"]
    styleH.alignment = 1

    story = []

    # Logo superior
    logo_path = "static/base/born/images/logo.png"
    try:
        img = Image(logo_path, width=120, height=120)
        img.hAlign = "CENTER"
        story.append(img)
        story.append(Spacer(1, 12))
    except:
        story.append(Paragraph("LOGO NO ENCONTRADO", styleN))

    # Título principal
    story.append(Paragraph("<b>CERTIFICADO OFICIAL DE RESIDENCIA – CENSO 2025</b>", styleH))
    story.append(Spacer(1, 12))

    # Texto del cuerpo
    texto = f"""
    El Resguardo Indígena Muisca de Chía CERTIFICA que:

    <br/><br/>
    <b>{persona.primer_nombre or ''} {persona.segun_nombre or ''} {persona.primer_apellido or ''} {persona.segun_apellido or ''}</b>,
    identificado(a) con documento <b>{persona.tipo_ident or ''} No. {persona.num_doc}</b>,
    aparece registrado(a) en el proceso del <b>Censo General del Resguardo – Vigencia 2025</b>,
    en calidad de integrante de la comunidad.

    <br/><br/>
    Datos adicionales:
    <br/>• Sexo: <b>{persona.sexo or ''}</b>
    <br/>• Edad: <b>{persona.edad or ''}</b>
    <br/>• Sector: <b>{persona.sector_cnmbr or ''}</b>
    <br/>• Comunidad: <b>{persona.comunid_cnmbr or ''}</b>
    <br/>• Fecha de registro: <b>{persona.v_fecha.date() if persona.v_fecha else ''}</b>

    <br/><br/>
    Este certificado se expide a solicitud del interesado para fines institucionales y legales.
    """

    story.append(Paragraph(texto, styleN))
    story.append(Spacer(1, 20))

    # QR de verificación
    qr_data = f"http://138.68.16.55:8011/verificar/{doc}/"
    qr_img = qrcode.make(qr_data)
    qr_buffer = BytesIO()
    qr_img.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)

    qr_rl_img = Image(qr_buffer, width=120, height=120)
    qr_rl_img.hAlign = "CENTER"
    story.append(qr_rl_img)
    story.append(Spacer(1, 6))
    story.append(Paragraph("<i>Escanee el código para verificar la autenticidad</i>", styleN))

    # Firma
    story.append(Spacer(1, 25))
    story.append(Paragraph("<b>_____________________________<br/>Autoridad del Resguardo</b>", styleN))

    # Pie de página
    story.append(Spacer(1, 12))
    fecha = datetime.date.today().strftime("%d/%m/%Y")
    story.append(Paragraph(f"<i>Emitido el {fecha}</i>", styleN))

    pdf.build(story)

    buffer.seek(0)
    return HttpResponse(buffer, content_type="application/pdf")