from django.test import TestCase
from django.urls import reverse
from .models import AboutMePost


class PageTests(TestCase):
    def test_url_exist_at_correct_location(self):
        response_by_path = self.client.get("/yo")
        response_by_name = self.client.get(reverse("about_me"))
        self.assertEqual(response_by_path.status_code, 200)
        self.assertEqual(response_by_name.status_code, 200)

    def test_url_use_correct_template(self):
        response = self.client.get(reverse("about_me"))
        self.assertTemplateUsed(response, "about_me.html")

    def test_non_existent_page_returns_404(self):
        response = self.client.get("/pagina-no-existe")
        self.assertEqual(response.status_code, 404)


class AboutMePostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entry = AboutMePost.objects.create(title="yo titulo", body="yo cuerpo")

    def test_page_contains_text(self):
        response = self.client.get(reverse("about_me"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.entry.title)
