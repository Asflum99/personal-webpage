from pages.admin import custom_admin_site
from django.urls import path, include
from two_factor.urls import urlpatterns as tf_urls
from coding_journal.settings import ADMIN_PANEL

urlpatterns = [
    path("", include("pages.journal.urls")),
    path(ADMIN_PANEL, custom_admin_site.urls),
    path("yo", include("pages.about_me.urls")),
    path("tinymce/", include("tinymce.urls")),
    path("accounts/", include(tf_urls)),
]
