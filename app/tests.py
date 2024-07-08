from django.test import TestCase
from django.urls import reverse, resolve
from .views import hello, form
        

class UrlsTestCase(TestCase):
    def test_hello_url_is_resolved(self):
        url = reverse('hello')
        self.assertEqual(resolve(url).func, hello)

    def test_form_url_is_resolved(self):
        url = reverse('form')
        self.assertEqual(resolve(url).func, form)

class ViewsTestCase(TestCase):
    def test_hello_view(self):
        response = self.client.get(reverse('hello'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hello.html')

    def test_form_view(self):
        response = self.client.get(reverse('form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
 
