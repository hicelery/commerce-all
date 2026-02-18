from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .forms import ContactForm
from .models import Contact, AboutPage


class TestAboutViews(TestCase):

    def setUp(self):
        self.AboutPage = AboutPage(
            title="About Me", content="This is about me.", author="Author Name")
        self.AboutPage.save()

    def test_render_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"About Me", response.content)
        self.assertIn(b"This is about me.", response.content)
        self.assertIsInstance(
            response.context['contact_form'], ContactForm)
        print(response.content)

    def test_successful_contact_request_submission(self):
        """Test for a user submitting a contact request"""
        post_data = {
            'name': 'test name',
            'email': 'test@email.com',
            'message': 'test message'
        }
        response = self.client.post(reverse('about'), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'Contact request submitted successfully', response.content)
