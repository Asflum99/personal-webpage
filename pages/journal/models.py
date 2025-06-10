from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from tinymce.models import HTMLField


class Entry(models.Model):
    """
    Modelo que representa una entrada del diario, con título, contenido,
    etiqueta y fecha de creación.
    """

    title = models.CharField(max_length=100)
    body = HTMLField()
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(editable=False, max_length=100)

    # Opciones de etiquetas para clasificar las entradas
    NOTES = "NT"
    LEARNING = "LR"

    # Lo primero es la etiqueta que guardará en la base de datos y lo segundo es lo que aparecerá en el panel de administración
    TAGS = [
        (NOTES, "Notas"),
        (LEARNING, "Aprendiendo"),
    ]
    tag = models.CharField(
        max_length=2,
        choices=TAGS,
        default=LEARNING,
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        if self.tag == self.NOTES:
            return reverse("notes_entry", kwargs={"slug": self.slug})
        return reverse("learning_entry", kwargs={"slug": self.slug})

    class Meta:
        verbose_name_plural = "Entradas"
