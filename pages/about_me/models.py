from django.db import models
from tinymce.models import HTMLField


class AboutMePost(models.Model):
    """
    Modelo para almacenar la información de la sección "Acerca de mí"
    Contiene un título y un cuerpo
    """

    title = models.CharField(max_length=50)
    body = HTMLField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Acerca de mí"
