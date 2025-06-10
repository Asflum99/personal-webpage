from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify
from .models import Entry


class PageTests(TestCase):
    urls = [
        ("/", "home", "home.html", "Alvaro Flores"),
        ("/aprendiendo", "learning", "learning.html", "Esto es lo que estoy aprendiendo"),
        ("/notas", "notes", "notes.html", "Notas"),
    ]

    @classmethod
    def setUpTestData(cls):
        # Entradas para aprendiendo
        cls.learning1 = Entry.objects.create(
            title="aprendiendo 1", body="cuerpo prueba", tag=Entry.LEARNING
        )
        cls.learning2 = Entry.objects.create(
            title="aprendiendo 2", body="cuerpo prueba", tag=Entry.LEARNING
        )
        cls.learning3 = Entry.objects.create(
            title="aprendiendo 3", body="cuerpo prueba", tag=Entry.LEARNING
        )

        # Entradas para notas
        cls.notes1 = Entry.objects.create(
            title="notas 1", body="cuerpo prueba", tag=Entry.NOTES
        )
        cls.notes2 = Entry.objects.create(
            title="notas 2", body="cuerpo prueba", tag=Entry.NOTES
        )
        cls.notes3 = Entry.objects.create(
            title="notas 3", body="cuerpo prueba", tag=Entry.NOTES
        )
        
    def test_list_all_entries(self):
        tests = {
            "learning": [self.learning1, self.learning2, self.learning3],
            "notes": [self.notes1, self.notes2, self.notes3]
        }
        for page, entries in tests.items():
            with self.subTest(page=page):
                response = self.client.get(reverse(page))
                for entry in entries:
                    self.assertContains(response, entry.title)


    def test_url_exist_at_correct_location(self):
        for url, page, _, _ in self.urls:
            with self.subTest(page=page):
                response_by_path = self.client.get(url)
                response_by_name = self.client.get(reverse(page))
                self.assertEqual(response_by_path.status_code, 200)
                self.assertEqual(response_by_name.status_code, 200)

    def test_url_use_correct_template(self):
        for _, page, template, _ in self.urls:
            with self.subTest(template=template):
                response = self.client.get(reverse(page))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template)

    def test_pages_contains_text(self):
        for _, page, _, content in self.urls:
            with self.subTest(content=content):
                response = self.client.get(reverse(page))
                self.assertContains(response, content)

    def test_non_existent_page_returns_404(self):
        response = self.client.get("/pagina-no-existe")
        self.assertEqual(response.status_code, 404)


class EntryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entry = Entry.objects.create(
            title="titulo prueba", body="cuerpo prueba", tag=Entry.NOTES
        )

    def test_model_content(self):
        self.assertEqual(self.entry.title, "titulo prueba")
        self.assertEqual(self.entry.body, "cuerpo prueba")
        self.assertEqual(self.entry.tag, Entry.NOTES)

    def test_model_url(self):
        self.assertEqual(self.entry.get_absolute_url(), "/notas/titulo-prueba")

    def test_entry_detail_view(self):
        response = self.client.get(self.entry.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.entry.title)
    
    def test_entry_slug_in_url(self):
        expected_url = f"/notas/{slugify(self.entry.title)}"
        self.assertEqual(self.entry.get_absolute_url(), expected_url)
