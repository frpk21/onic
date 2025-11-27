from django.urls import path
from .views_sso import sso_callback_view

app_name = "accounts"

urlpatterns = [
    path("sso/callback/", sso_callback_view, name="sso_callback"),
]
