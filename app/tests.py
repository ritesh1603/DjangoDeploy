from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpRequest
from .views import hello, form

class URLTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_hello_url(self):
        response = self.client.get(reverse('hello'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hello.html')

    def test_form_url(self):
        response = self.client.get(reverse('form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_hello_view(self):
        request = HttpRequest()
        response = hello(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'The only way to learn is to live!', response.content)

    def test_form_view(self):
        request = HttpRequest()
        response = form(request)
        self.assertEqual(response.status_code, 200)
