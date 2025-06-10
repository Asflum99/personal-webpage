from django.contrib.admin import AdminSite, ModelAdmin
from pages.about_me.models import AboutMePost
from pages.journal.models import Entry

class EntryAdmin(ModelAdmin):
    list_display = ("title", "tag", "date")

    def save_model(self, request, obj, form, change):
        try:
            print(f"Intentando guardar Entry: title='{obj.title}', tag='{obj.tag}'")
            super().save_model(request, obj, form, change)
            print(f"Entry guardada con slug: {obj.slug}")
        except Exception as e:
            print(f"Error guardando Entry: {e}")
            raise


class MyAdminSite(AdminSite):
    # tu código actual para MyAdminSite...
    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request)
        new_dict = {
            "has_module_perms": True,
            "models": [],
            "name": "Páginas",
        }
        for app in app_list:
            new_dict["models"].extend(app["models"])
        new_list = [new_dict]
        return new_list


custom_admin_site = MyAdminSite(name="Custom admin")

custom_admin_site.register(AboutMePost)
custom_admin_site.register(Entry, EntryAdmin)
