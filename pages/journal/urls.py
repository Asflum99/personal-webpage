from django.urls import path

from .views import (
    HomePageView,
    LearningView,
    NotesView,
    NotesDetailView,
    LearningDetailView,
    upload_image,
    get_image_list,
    delete_image
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("aprendiendo", LearningView.as_view(), name="learning"),
    path("notas", NotesView.as_view(), name="notes"),
    path("notas/<slug:slug>", NotesDetailView.as_view(), name="notes_entry"),
    path("aprendiendo/<slug:slug>", LearningDetailView.as_view(), name="learning_entry"),
    path("upload_image/", upload_image, name="upload_image"),
    path("image_list/", get_image_list, name="image_list"),
    path("delete_image/", delete_image, name="delete_image"),
]
