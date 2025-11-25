from django.urls import path
from .views_sso import sso_callback_view

urlpatterns = [
    path("sso/callback/", sso_callback_view, name="sso_callback"),
]
