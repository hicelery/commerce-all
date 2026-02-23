from django.test import TestCase
from .forms import ContactForm


class TestCollaborateForm(TestCase):

    def test_form_is_valid(self):
        """ Test for all fields"""
        form = ContactForm({
            'name': 'test name',
            'email': 'test@test.com',
            'type': 'general',
            'message': 'Hello!'
        })
        self.assertTrue(form.is_valid(),
                        msg=f"Form is not valid errors: {form.errors}")
