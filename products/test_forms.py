from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from .forms import ReviewForm
from .models import Product, Category


class TestReviewFormValidation(TestCase):
    """Test ReviewForm validation"""

    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            brand="Brand",
            colour="Red",
            size="M",
            description="Description",
            price=Decimal("29.99"),
            category=self.category
        )
        self.user = User.objects.create_user(
            username="testuser",
            password="pass123",
            email="test@test.com"
        )
        self.staff_user = User.objects.create_user(
            username="staffuser",
            password="pass123",
            email="staff@test.com",
            is_staff=True
        )

    def test_valid_form_all_fields(self):
        """Test form is valid with all required fields"""
        form_data = {
            'rating': 5,
            'title': 'Great product!',
            'comment': 'I enjoyed using this product. Highly recommend!',
        }
        form = ReviewForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")

    def test_form_missing_rating(self):
        """Test form is invalid when rating is missing"""
        form_data = {
            'title': 'Great product!',
            'comment': 'I really enjoyed using this product.',
        }
        form = ReviewForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_form_missing_title(self):
        """Test form is invalid when title is missing"""
        form_data = {
            'rating': 5,
            'comment': 'I really enjoyed using this product.',
        }
        form = ReviewForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_form_missing_comment(self):
        """Test form is invalid when comment is missing"""
        form_data = {
            'rating': 5,
            'title': 'Great product!',
        }
        form = ReviewForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('comment', form.errors)

    def test_form_with_minimum_rating(self):
        """Test form with minimum rating of 1"""
        form_data = {
            'rating': 1,
            'title': 'Not good',
            'comment': 'Poor product',
        }
        form = ReviewForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_form_with_maximum_rating(self):
        """Test form with maximum rating of 5"""
        form_data = {
            'rating': 5,
            'title': 'Excellent',
            'comment': 'Excellent product',
        }
        form = ReviewForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_form_with_empty_title(self):
        """Test form with empty title is invalid"""
        form_data = {
            'rating': 5,
            'title': '',
            'comment': 'Good product',
        }
        form = ReviewForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())

    def test_form_with_empty_comment(self):
        """Test form with empty comment is invalid"""
        form_data = {
            'rating': 5,
            'title': 'Good',
            'comment': '',
        }
        form = ReviewForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())

    def test_form_with_long_title(self):
        """Test form with very long title"""
        form_data = {
            'rating': 4,
            'title': 'A' * 255,  # Max length is 255
            'comment': 'Good product',
        }
        form = ReviewForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_regular_user_cannot_see_approved_field(self):
        """Test that regular users cannot see the approved field"""
        form = ReviewForm(user=self.user)
        self.assertNotIn('approved', form.fields)

    def test_staff_user_can_see_approved_field(self):
        """Test that staff users can see the approved field"""
        form = ReviewForm(user=self.staff_user)
        self.assertIn('approved', form.fields)

    def test_form_without_user_removes_approved_field(self):
        """Test that form without user removes approved field"""
        form = ReviewForm()
        self.assertNotIn('approved', form.fields)

    def test_staff_user_can_approve_in_form(self):
        """Test staff user can set approved flag"""
        form_data = {
            'rating': 5,
            'title': 'Great!',
            'comment': 'Great product',
            'approved': True
        }
        form = ReviewForm(data=form_data, user=self.staff_user)
        self.assertTrue(form.is_valid())

    def test_regular_user_cannot_approve_in_form(self):
        """Test regular user cannot pass approved field to form"""
        form_data = {
            'rating': 5,
            'title': 'Great!',
            'comment': 'Great product',
            'approved': True
        }
        form = ReviewForm(data=form_data, user=self.user)
        # Form should still be valid but approved field should be ignored
        self.assertTrue(form.is_valid())
        self.assertNotIn('approved', form.fields)

    def test_form_with_unicode_characters(self):
        """Test form with unicode characters"""
        form_data = {
            'rating': 5,
            'title': 'Très bon! 日本語',
            'comment': 'اللغة العربية and other unicode: 🎉',
        }
        form = ReviewForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_form_rating_validation_not_integer(self):
        """Test form with non-integer rating"""
        form_data = {
            'rating': 'five',  # Invalid - should be integer
            'title': 'Great',
            'comment': 'Good',
        }
        form = ReviewForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())

    def test_form_fields(self):
        """Test form has expected fields"""
        form = ReviewForm(user=self.user)
        expected_fields = {'rating', 'title', 'comment'}
        self.assertEqual(set(form.fields.keys()), expected_fields)
