from typing import Any
from django.utils.text import slugify
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage
from django.views.generic import ListView, DetailView
from django.contrib.admin.views.decorators import staff_member_required
from .models import Entry
from collections import defaultdict
from urllib.parse import quote
import calendar, locale, os, boto3


locale.setlocale(locale.LC_TIME, "es_PE.UTF-8")


def group_entries_by_year_and_month(entries):
    years = defaultdict(
        lambda: defaultdict(list)
    )  # Crea un diccionario cuyo valor predeterminado es otro diccionario cuyo valor predeterminado es una lista vacía

    for entry in entries:
        entry_year = entry.date.year
        entry_month = entry.date.month
        month_name = str(calendar.month_name[entry_month]).capitalize()
        years[entry_year][month_name].append(
            entry
        )  # Si no existe la clave, la crea junto a su valor predeterminado

    # Convertir defaultdict en un diccionario estándar
    return {year: dict(months) for year, months in years.items()}


class HomePageView(ListView):
    model = Entry
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["learning_posts"] = Entry.objects.filter(tag=Entry.LEARNING).order_by(
            "-date"
        )[:3]
        context["notes_posts"] = Entry.objects.filter(tag=Entry.NOTES).order_by(
            "-date"
        )[:3]
        return context


class NotesView(ListView):
    model = Entry
    template_name = "notes.html"

    def get_queryset(self):
        return Entry.objects.filter(tag=Entry.NOTES).order_by("-date")

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        entries = self.get_queryset()
        context["grouped_entries"] = group_entries_by_year_and_month(entries)
        return context


class NotesDetailView(DetailView):
    model = Entry
    template_name = "notes_entry.html"


class LearningView(ListView):
    model = Entry
    template_name = "learning.html"

    def get_queryset(self):
        return Entry.objects.filter(tag=Entry.LEARNING).order_by("-date")

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        entries = self.get_queryset()
        context["grouped_entries"] = group_entries_by_year_and_month(entries)
        return context


class LearningDetailView(DetailView):
    model = Entry
    template_name = "learning_entry.html"


@staff_member_required
def upload_image(request):
    if request.method != "POST":
        return JsonResponse({"Error Message": "Wrong request"})

    try:
        file_obj = request.FILES["file"]
        file_name = file_obj.name
        root, ext = os.path.splitext(file_name)
        if ext.lower() not in [".png", ".jpg", ".jpeg"]:
            return JsonResponse(
                {
                    "error": f"Error en el sufijo del archivo ({ext}), los permitidos son .jpg, .png y .jpeg"
                }
            )
        file_name_slugify = slugify(root) + ext
        saved_path = default_storage.save(file_name_slugify, file_obj)
        return JsonResponse(
            {
                "location": f"{settings.MEDIA_URL}{saved_path}",
            }
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_image_list(request):
    images = []

    # Crear cliente S3
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    # Listar objetos del bucket
    response = s3.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)

    if "Contents" in response:
        for obj in response["Contents"]:
            key = obj["Key"]
            if key.lower().endswith((".png", ".jpg", ".jpeg")):
                images.append(
                    {
                        "url": f"{settings.MEDIA_URL}{key}",
                        "text": key,
                        "safe_id": quote(key),
                    }
                )

    # Devolver siempre un JSON válido
    return JsonResponse({"empty": len(images) == 0, "images": images}, safe=False)


@staff_member_required
def delete_image(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    try:
        filename = request.POST.get("filename")
        if not filename:
            return JsonResponse({"error": "Archivo no proporcionado"}, status=400)

        s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=filename)
        return JsonResponse({"message": "Imagen eliminada exitosamente."})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
