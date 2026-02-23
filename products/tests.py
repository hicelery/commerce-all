from django.test import TestCase
from .models import Product, Category
from django.contrib.auth.models import User


class TestProductModel(TestCase):

    def setUp(self):
        self.category = Category(
            name="Electronics")
        self.category.save()

        self.product = Product(
            name="Test Product",
            brand="Test Brand",
            colour="Test Colour",
            size="Test Size",
            description="Test Description",
            price=29.99,
            category=self.category
        )
        self.product.save()

    def test_product_creation(self):
        """Test that a product can be created"""
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.price, 29.99)
        self.assertEqual(self.product.brand, "Test Brand")

    def test_product_string_representation(self):
        """Test product model string output"""
        self.assertEqual(str(self.product), "Test Brand Test Product (Test Colour, Test Size)")

    def test_product_category_relationship(self):
        """Test product category relationship"""
        self.assertEqual(self.product.category, self.category)
        self.assertIn(self.product, self.category.products.all())

    def test_product_category_creation(self):
        """Test that a category can be created"""
        self.assertEqual(self.category.name, "Electronics")
