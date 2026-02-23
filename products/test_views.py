from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .forms import ReviewForm
from .models import Product, Category, ProductSize, ProductImage, ProductReview, ProductDiscount, DiscountCode


class TestProductViews(TestCase):
    """ Test cases for product views """

    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            category=self.category,
            price=99.99,
            description="Test Description"
        )
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="test1@test.com"
        )

    def test_product_list_view(self):
        response = self.client.get(reverse('products:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_detail_view(self):
        response = self.client.get(
            reverse('products:product_detail', args=[self.product.product_id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'], self.product)

    def test_product_review_form_valid(self):
        form_data = {
            'product': self.product.product_id,
            'user': self.user.id,
            'rating': 5,
            'title': 'Great product!',
            'comment': 'Great product!'
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_product_review_form_invalid(self):
        form_data = {'rating': 6}
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_product_review(self):
        review = ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment="Good quality"
        )
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.user, self.user)
