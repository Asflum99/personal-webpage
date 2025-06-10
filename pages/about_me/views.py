from typing import Any
from django.views.generic import TemplateView
from .models import AboutMePost


class AboutView(TemplateView):
    """
    Vista para mostrar la información del modelo AboutMePost en la plantilla.
    """

    model = AboutMePost
    template_name = "about_me.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["about"] = AboutMePost.objects.first()
        return context
