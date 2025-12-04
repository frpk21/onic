from django.urls import path
from dashboard.views import DashboardSummary, PiramideAPIView
from dashboard import views

urlpatterns = [
    path("api/summary/", DashboardSummary.as_view(), name="summary"),
    path("api/piramide/", PiramideAPIView.as_view(), name="piramide"),
    path("", views.dashboard_page, name="dashboard_page"),
    path("api/sectores/", views.SectorPoblacionAPIView.as_view(), name="sectores"),
    path("api/edad-resumen/", views.EdadResumenAPIView.as_view(), name="edad_resumen"),
    path("api/estado-civil/", views.EstadoCivilAPIView.as_view(), name="estado_civil"),
    path("api/educacion/", views.EducacionAPIView.as_view(), name="educacion"),
    path("api/ocupacion/", views.OcupacionAPIView.as_view(), name="ocupacion"),
    path("api/salud/", views.SaludAPIView.as_view(), name="salud"),
    path("api/migracion/", views.MigracionAPIView.as_view(), name="migracion"),
    path("api/vivienda/", views.ViviendaAPIView.as_view(), name="vivienda"),
    path("certificado/", views.certificado_buscar, name="certificado_buscar"),
    path("certificado/pdf/<str:doc>/", views.certificado_pdf, name="certificado_pdf"),
]
