from django.test import TestCase
from .models import AboutPage, Contact, OrderQuery


class TestAboutPageModel(TestCase):
    """Test AboutPage model"""

    def test_aboutpage_creation(self):
        """Test creating an AboutPage"""
        about = AboutPage.objects.create(
            title="About Us",
            content="This is our company story",
            author="John Doe"
        )
        self.assertEqual(about.title, "About Us")
        self.assertEqual(about.author, "John Doe")

    def test_aboutpage_string_representation(self):
        """Test AboutPage string representation"""
        about = AboutPage.objects.create(
            title="Our Story",
            content="Content here",
            author="Jane Doe"
        )
        self.assertEqual(str(about), "Our Story by Jane Doe")

    def test_aboutpage_updated_on_timestamp(self):
        """Test that updated_on timestamp is set"""
        about = AboutPage.objects.create(
            title="Test",
            content="Test content",
            author="Test Author"
        )
        self.assertIsNotNone(about.updated_on)

    def test_aboutpage_long_content(self):
        """Test AboutPage with long content"""
        long_content = "A" * 5000
        about = AboutPage.objects.create(
            title="Long Content",
            content=long_content,
            author="Author"
        )
        self.assertEqual(len(about.content), 5000)


class TestContactModel(TestCase):
    """Test Contact model"""

    def test_contact_creation(self):
        """Test creating a contact request"""
        contact = Contact.objects.create(
            name="John Smith",
            email="john@example.com",
            message="Hello, I want to collaborate",
            type="collaboration"
        )
        self.assertEqual(contact.name, "John Smith")
        self.assertEqual(contact.email, "john@example.com")
        self.assertEqual(contact.type, "collaboration")

    def test_contact_string_representation(self):
        """Test Contact string representation"""
        contact = Contact.objects.create(
            name="Alice",
            email="alice@example.com",
            message="Test message",
            type="general"
        )
        self.assertEqual(str(contact), "Contact request from Alice")

    def test_contact_default_read_status(self):
        """Test that read defaults to False"""
        contact = Contact.objects.create(
            name="Bob",
            email="bob@example.com",
            message="Message",
            type="bug report"
        )
        self.assertFalse(contact.read)

    def test_contact_read_status_true(self):
        """Test setting contact read status to True"""
        contact = Contact.objects.create(
            name="Carol",
            email="carol@example.com",
            message="Message",
            type="general",
            read=True
        )
        self.assertTrue(contact.read)

    def test_contact_type_choices(self):
        """Test all contact type choices"""
        types = ["bug report", "collaboration", "general"]
        for contact_type in types:
            contact = Contact.objects.create(
                name=f"User {contact_type}",
                email=f"{contact_type}@example.com",
                message="Test",
                type=contact_type
            )
            self.assertEqual(contact.type, contact_type)


class TestOrderQueryModel(TestCase):
    """Test OrderQuery model"""

    def test_order_query_creation(self):
        """Test creating an order query"""
        query = OrderQuery.objects.create(
            name="Emma",
            email="emma@example.com",
            order_id="ORD-12345",
            message="Where is my order?"
        )
        self.assertEqual(query.name, "Emma")
        self.assertEqual(query.order_id, "ORD-12345")

    def test_order_query_string_representation(self):
        """Test OrderQuery string representation"""
        query = OrderQuery.objects.create(
            name="Frank",
            email="frank@example.com",
            order_id="ORD-67890",
            message="Question about order"
        )
        self.assertEqual(str(query), "Order query from Frank")

    def test_order_query_without_order_id(self):
        """Test OrderQuery with no order_id (null and blank allowed)"""
        query = OrderQuery.objects.create(
            name="Grace",
            email="grace@example.com",
            message="General order question"
        )
        self.assertIsNone(query.order_id)

    def test_order_query_default_read_status(self):
        """Test that read defaults to False"""
        query = OrderQuery.objects.create(
            name="Henry",
            email="henry@example.com",
            message="Order inquiry"
        )
        self.assertFalse(query.read)

    def test_order_query_read_status_true(self):
        """Test setting order query read status to True"""
        query = OrderQuery.objects.create(
            name="Iris",
            email="iris@example.com",
            order_id="ORD-99999",
            message="Follow up",
            read=True
        )
        self.assertTrue(query.read)
