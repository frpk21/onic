import jwt
from django.conf import settings
from django.contrib.auth import login, get_user_model
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect


User = get_user_model()


def sso_callback_view(request):
    token = request.GET.get("token")
    if not token:
        return HttpResponseBadRequest("Missing token")

    try:
        # Verificar token usando el SECRET de smt_onic
        payload = jwt.decode(
            token,
            settings.SSO_SECRET,
            algorithms=["HS256"],
        )
    except jwt.ExpiredSignatureError:
        return HttpResponseBadRequest("Token expired")
    except jwt.InvalidTokenError:
        return HttpResponseBadRequest("Invalid token")

    username = payload.get("sub")
    email = payload.get("email")
    if not username:
        return HttpResponseBadRequest("Missing username in token")

    # Buscar o crear usuario en smt_onic
    user, created = User.objects.get_or_create(username=username)

    # Actualizar email si el usuario no tiene
    if email and not user.email:
        user.email = email
        user.save()

    # Iniciar sesión localmente
    login(request, user)

    # Redirigir a home (o a next si lo implementamos después)
    return redirect("/")
