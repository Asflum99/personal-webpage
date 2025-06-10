from django.http import HttpResponseForbidden
from coding_journal import settings
from coding_journal.settings import ADMIN_PANEL


class AdminAccessMiddleware:
    """Middleware para restringir el acceso al panel de administración según IP"""

    ALLOWED_IPS = settings.env.str("ALLOWED_IPS").split(",")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/{ADMIN_PANEL}"):
            ip = self.get_client_ip(request)
            if ip not in self.ALLOWED_IPS:
                return HttpResponseForbidden(
                    "No tienes permisos para acceder a esta página."
                )
        return self.get_response(request)

    def get_client_ip(self, request):
        """Obtiene la IP del cliente, considerando posibles proxies"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
