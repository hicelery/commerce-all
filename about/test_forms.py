from django.test import TestCase
from .forms import ContactForm, OrderForm


class TestContactFormValidation(TestCase):
    """Test ContactForm validation"""

    def test_contact_form_valid_data(self):
        """Test form with valid data"""
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'type': 'general',
            'message': 'I would like to inquire about your services'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")

    def test_contact_form_missing_name(self):
        """Test form is invalid without name"""
        form_data = {
            'email': 'john@example.com',
            'type': 'general',
            'message': 'Hello'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_contact_form_missing_email(self):
        """Test form is invalid without email"""
        form_data = {
            'name': 'John Doe',
            'type': 'general',
            'message': 'Hello'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_contact_form_missing_message(self):
        """Test form is invalid without message"""
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'type': 'general'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)

    def test_contact_form_missing_type(self):
        """Test form is invalid without type"""
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'Hello'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('type', form.errors)

    def test_contact_form_invalid_email(self):
        """Test form with invalid email format"""
        form_data = {
            'name': 'John Doe',
            'email': 'not-an-email',
            'type': 'general',
            'message': 'Hello'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_contact_form_all_type_choices(self):
        """Test form with all available types"""
        types = ['bug report', 'collaboration', 'general']
        for contact_type in types:
            form_data = {
                'name': 'John Doe',
                'email': 'john@example.com',
                'type': contact_type,
                'message': 'Test message'
            }
            form = ContactForm(data=form_data)
            self.assertTrue(form.is_valid(),
                            f"Type {contact_type} should be valid")

    def test_contact_form_empty_message(self):
        """Test form with empty message"""
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'type': 'general',
            'message': ''
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestOrderFormValidation(TestCase):
    """Test OrderForm validation"""

    def test_order_form_valid_with_order_id(self):
        """Test order form with all fields including order_id"""
        form_data = {
            'name': 'Emma Smith',
            'email': 'emma@example.com',
            'order_id': 'ORD-12345',
            'message': 'Where is my order?'
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")

    def test_order_form_valid_without_order_id(self):
        """Test order form without order_id (optional field)"""
        form_data = {
            'name': 'Emma Smith',
            'email': 'emma@example.com',
            'message': 'General order question'
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_order_form_missing_name(self):
        """Test form is invalid without name"""
        form_data = {
            'email': 'emma@example.com',
            'order_id': 'ORD-12345',
            'message': 'Test'
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_order_form_missing_email(self):
        """Test form is invalid without email"""
        form_data = {
            'name': 'Emma Smith',
            'order_id': 'ORD-12345',
            'message': 'Test'
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_order_form_missing_message(self):
        """Test form is invalid without message"""
        form_data = {
            'name': 'Emma Smith',
            'email': 'emma@example.com',
            'order_id': 'ORD-12345'
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)

    def test_order_form_invalid_email(self):
        """Test form with invalid email"""
        form_data = {
            'name': 'Emma Smith',
            'email': 'invalid-email',
            'order_id': 'ORD-12345',
            'message': 'Test'
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_order_form_empty_order_id(self):
        """Test form with empty order_id (optional field)"""
        form_data = {
            'name': 'Emma Smith',
            'email': 'emma@example.com',
            'order_id': '',
            'message': 'Test'
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_order_form_special_characters(self):
        """Test form with special characters"""
        form_data = {
            'name': "O'Brien & Co.",
            'email': 'obrien+special@example.com',
            'order_id': 'ORD-2024-001/A',
            'message': 'Question about order: #12345 & refund!'
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())
