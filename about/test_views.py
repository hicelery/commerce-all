from django.test import TestCase, Client
from django.urls import reverse
from .forms import ContactForm, OrderForm
from .models import Contact, AboutPage, OrderQuery


class TestAboutDetailView(TestCase):
    """Test about_detail view"""

    def setUp(self):
        self.client = Client()
        self.about = AboutPage.objects.create(
            title="About Us",
            content="We are a great company",
            author="Company Team"
        )

    def test_about_detail_view_loads(self):
        """Test about_detail view returns 200 status"""
        response = self.client.get(reverse('about:about'))
        self.assertEqual(response.status_code, 200)

    def test_about_detail_displays_content(self):
        """Test about page content is displayed"""
        response = self.client.get(reverse('about:about'))
        self.assertContains(response, "About Us")
        self.assertContains(response, "We are a great company")

    def test_about_detail_context_has_about(self):
        """Test context contains about page object"""
        response = self.client.get(reverse('about:about'))
        self.assertEqual(response.context['about'], self.about)

    def test_about_detail_context_has_form(self):
        """Test context contains contact form"""
        response = self.client.get(reverse('about:about'))
        self.assertIn('contact_form', response.context)
        self.assertIsInstance(response.context['contact_form'], ContactForm)

    def test_about_detail_uses_correct_template(self):
        """Test correct template is used"""
        response = self.client.get(reverse('about:about'))
        self.assertTemplateUsed(response, 'about/about.html')

    def test_about_detail_no_about_page(self):
        """Test view when no AboutPage exists"""
        AboutPage.objects.all().delete()
        response = self.client.get(reverse('about:about'))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['about'])

    def test_about_detail_multiple_pages_shows_first(self):
        """Test that first() returns only first page when multiple exist"""
        AboutPage.objects.create(
            title="Second Page",
            content="This is second",
            author="Author 2"
        )
        response = self.client.get(reverse('about:about'))
        self.assertEqual(response.context['about'].title, "About Us")

    def test_about_detail_post_valid_contact_form(self):
        """Test submitting valid contact form"""
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'type': 'collaboration',
            'message': 'I want to collaborate'
        }
        response = self.client.post(reverse('about:about'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Contact.objects.filter(name='John Doe').exists())

    def test_about_detail_post_contact_creates_record(self):
        """Test that POST creates a Contact record"""
        form_data = {
            'name': 'Jane Smith',
            'email': 'jane@example.com',
            'type': 'bug report',
            'message': 'Found a bug'
        }
        self.client.post(reverse('about:about'), form_data)
        contact = Contact.objects.get(name='Jane Smith')
        self.assertEqual(contact.email, 'jane@example.com')
        self.assertEqual(contact.type, 'bug report')

    def test_about_detail_post_invalid_contact_form(self):
        """Test posting invalid contact form data"""
        form_data = {
            'name': 'John Doe',
            'email': 'invalid-email',
            'type': 'general',
            'message': 'Hello'
        }
        response = self.client.post(reverse('about:about'), form_data)
        self.assertEqual(response.status_code, 200)
        # Contact should not be created for invalid email
        self.assertFalse(Contact.objects.filter(name='John Doe').exists())


class TestOrderContactView(TestCase):
    """Test Ordercontact view"""

    def setUp(self):
        self.client = Client()

    def test_order_contact_view_loads(self):
        """Test Ordercontact view returns 200 status"""
        response = self.client.get(reverse('about:contact'))
        self.assertEqual(response.status_code, 200)

    def test_order_contact_uses_correct_template(self):
        """Test correct template is used"""
        response = self.client.get(reverse('about:contact'))
        self.assertTemplateUsed(response, 'about/contact.html')

    def test_order_contact_context_has_form(self):
        """Test context contains order form"""
        response = self.client.get(reverse('about:contact'))
        self.assertIn('order_form', response.context)
        self.assertIsInstance(response.context['order_form'], OrderForm)

    def test_order_contact_post_valid_form(self):
        """Test submitting valid order form"""
        form_data = {
            'name': 'Emma Davis',
            'email': 'emma@example.com',
            'order_id': 'ORD-12345',
            'message': 'Where is my order?'
        }
        response = self.client.post(reverse('about:contact'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(OrderQuery.objects.filter(name='Emma Davis').exists())

    def test_order_contact_post_creates_record(self):
        """Test that POST creates an OrderQuery record"""
        form_data = {
            'name': 'Frank Miller',
            'email': 'frank@example.com',
            'order_id': 'ORD-67890',
            'message': 'Need to track my package'
        }
        self.client.post(reverse('about:contact'), form_data)
        query = OrderQuery.objects.get(name='Frank Miller')
        self.assertEqual(query.email, 'frank@example.com')
        self.assertEqual(query.order_id, 'ORD-67890')

    def test_order_contact_post_without_order_id(self):
        """Test submitting order form without order_id"""
        form_data = {
            'name': 'Grace Lee',
            'email': 'grace@example.com',
            'message': 'General order question'
            # order_id is optional
        }
        response = self.client.post(reverse('about:contact'), form_data)
        self.assertEqual(response.status_code, 200)
        query = OrderQuery.objects.get(name='Grace Lee')
        self.assertIsNone(query.order_id)

    def test_order_contact_post_invalid_email(self):
        """Test posting with invalid email"""
        form_data = {
            'name': 'Henry Brown',
            'email': 'not-an-email',
            'order_id': 'ORD-11111',
            'message': 'Test'
        }
        response = self.client.post(reverse('about:contact'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(OrderQuery.objects.filter(
            name='Henry Brown').exists())

    def test_order_contact_post_missing_required_field(self):
        """Test posting with missing required field"""
        form_data = {
            'name': 'Iris Chen',
            'email': 'iris@example.com'
            # Missing message
        }
        response = self.client.post(reverse('about:contact'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(OrderQuery.objects.filter(name='Iris Chen').exists())

    def test_order_contact_get_fresh_form(self):
        """Test GET request provides fresh form"""
        response = self.client.get(reverse('about:contact'))
        form = response.context['order_form']
        # Form should not have data
        self.assertIsNone(form.instance.pk)

    def test_order_contact_post_empty_form(self):
        """Test posting with empty form data"""
        response = self.client.post(reverse('about:contact'), {})
        self.assertEqual(response.status_code, 200)
        # No OrderQuery should be created
        self.assertEqual(OrderQuery.objects.count(), 0)
