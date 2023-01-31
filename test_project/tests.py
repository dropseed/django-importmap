from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.urls import reverse


class TestTemplate(TestCase):
    def setUp(self):
        self.client = Client()

    @override_settings(DEBUG=False)
    def test_template_output(self):
        url = reverse("index")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, "es-module-shims.js")

        self.assertContains(response, "react@17.0.2/index.js")

    @override_settings(DEBUG=True)
    def test_template_output_dev(self):
        url = reverse("index")
        response = self.client.get(url)
        # print(response.content.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, "es-module-shims.js")

        self.assertContains(response, "react@17.0.2/dev.index.js")

    @override_settings(DEBUG=False)
    def test_jinja_template_output(self):
        url = reverse("index_jinja")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "es-module-shims.js")

        self.assertContains(response, "react@17.0.2/index.js")

        self.assertContains(response, "/static/myjs.js")

    @override_settings(DEBUG=True)
    def test_jinja_template_output_dev(self):
        url = reverse("index_jinja")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "es-module-shims.js")

        self.assertContains(response, "react@17.0.2/dev.index.js")

        self.assertContains(response, "/static/myjs.js")
