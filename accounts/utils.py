from urllib.parse import urlencode

from django.conf import settings
from django.urls import reverse


def get_sso_login_url(request):
    callback_path = reverse("accounts:sso_callback")
    redirect_url = request.build_absolute_uri(callback_path)

    query = urlencode({
        "client_id": settings.SSO_CLIENT_ID,
        "redirect_url": redirect_url,
    })

    return f"{settings.AUTH_SERVER_BASE_URL}/auth/login/?{query}"
