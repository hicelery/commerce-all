from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client
from decimal import Decimal
from .models import (
    Product, Category, ProductSize, ProductImage, ProductReview,
)


class TestProductListView(TestCase):
    """Test ProductList view"""

    def setUp(self):
        self.client = Client()
        self.category1 = Category.objects.create(name="Electronics")
        self.category2 = Category.objects.create(name="Clothing")
        self.product1 = Product.objects.create(
            name="Laptop",
            brand="Dell",
            colour="Black",
            size="15",
            description="Good laptop",
            price=Decimal("999.99"),
            category=self.category1,
            quantity=10
        )
        self.product2 = Product.objects.create(
            name="T-Shirt",
            brand="Nike",
            colour="Blue",
            size="M",
            description="Good shirt",
            price=Decimal("29.99"),
            category=self.category2,
            quantity=50
        )
        self.product3 = Product.objects.create(
            name="Keyboard",
            brand="Logitech",
            colour="Black",
            size="Full",
            description="Mechanical keyboard",
            price=Decimal("149.99"),
            category=self.category1,
            quantity=5
        )

    def test_product_list_view_loads(self):
        """Test ProductList view returns 200 status"""
        response = self.client.get(reverse('products:home'))
        self.assertEqual(response.status_code, 200)

    def test_product_list_displays_all_products(self):
        """Test ProductList displays all products"""
        response = self.client.get(reverse('products:home'))
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)
        self.assertContains(response, self.product3.name)

    def test_product_list_category_filter(self):
        """Test ProductList filters by category"""
        url = reverse('products:home') + '?category_name=Electronics'
        response = self.client.get(url)
        self.assertContains(response, 'Laptop')
        self.assertContains(response, 'Keyboard')
        # Should not contain product from different category
        self.assertNotContains(response, 'T-Shirt')

    def test_product_list_category_filter_case_insensitive(self):
        """Test ProductList category filter is case-insensitive"""
        url = reverse('products:home') + '?category_name=electronics'
        response = self.client.get(url)
        self.assertContains(response, 'Laptop')
        self.assertContains(response, 'Keyboard')

    def test_product_list_category_filter_nonexistent(self):
        """Test ProductList with non-existent category"""
        url = reverse('products:home') + '?category_name=NonExistent'
        response = self.client.get(url)
        self.assertNotContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)

    def test_product_list_price_min_filter(self):
        """Test ProductList price minimum filter"""
        url = reverse('products:home') + '?price_min=100'
        response = self.client.get(url)
        self.assertContains(response, 'Laptop')
        self.assertContains(response, 'Keyboard')
        self.assertNotContains(response, 'T-Shirt')

    def test_product_list_price_max_filter(self):
        """Test ProductList price maximum filter"""
        url = reverse('products:home') + '?price_max=100'
        response = self.client.get(url)
        self.assertContains(response, 'T-Shirt')
        self.assertNotContains(response, 'Laptop')

    def test_product_list_price_range_filter(self):
        """Test ProductList price range filter"""
        url = reverse('products:home') + '?price_min=50&price_max=200'
        response = self.client.get(url)
        self.assertContains(response, 'Keyboard')
        self.assertNotContains(response, 'T-Shirt')
        self.assertNotContains(response, 'Laptop')

    def test_product_list_invalid_price_filter(self):
        """Test ProductList ignores invalid price filters"""
        url = reverse('products:home') + \
            '?price_min=invalid&price_max=notanumber'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.name)

    def test_product_list_sort_by_price_ascending(self):
        """Test ProductList sort by price ascending"""
        url = reverse('products:home') + '?sort=price_asc'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_list_sort_by_price_descending(self):
        """Test ProductList sort by price descending"""
        url = reverse('products:home') + '?sort=price_desc'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_list_sort_by_name(self):
        """Test ProductList sort by name"""
        url = reverse('products:home') + '?sort=name'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_list_sort_by_brand(self):
        """Test ProductList sort by brand"""
        url = reverse('products:home') + '?sort=brand'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_list_sort_by_newest(self):
        """Test ProductList sort by newest"""
        url = reverse('products:home') + '?sort=newest'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_list_sort_parameter_via_argument(self):
        """Test ProductList sort parameter via URL argument"""
        response = self.client.get(
            reverse('products:home') + '?sort_option=price_asc'
        )
        self.assertEqual(response.status_code, 200)

    def test_product_list_empty_products(self):
        """Test ProductList when no products exist"""
        Product.objects.all().delete()
        response = self.client.get(reverse('products:home'))
        self.assertEqual(response.status_code, 200)

    def test_product_list_contains_categories_context(self):
        """Test ProductList context contains all categories"""
        response = self.client.get(reverse('products:home'))
        self.assertIn('categories', response.context)
        categories = response.context['categories']
        self.assertIn(self.category1, categories)
        self.assertIn(self.category2, categories)


class TestProductDetailView(TestCase):
    """Test product_detail view"""

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Test Product",
            brand="Test Brand",
            colour="Black",
            size="M",
            description="Test description",
            price=Decimal("100.00"),
            category=self.category,
            quantity=10
        )
        self.user = User.objects.create_user(
            username="testuser",
            password="pass123",
            email="test@test.com"
        )

    def test_product_detail_view_loads(self):
        """Test product_detail view returns 200"""
        response = self.client.get(
            reverse('products:product_detail', args=[self.product.product_id])
        )
        self.assertEqual(response.status_code, 200)

    def test_product_detail_product_in_context(self):
        """Test product_detail includes product in context"""
        response = self.client.get(
            reverse('products:product_detail', args=[self.product.product_id])
        )
        self.assertEqual(response.context['product'], self.product)

    def test_product_detail_nonexistent_product(self):
        """Test product_detail with non-existent product"""
        response = self.client.get(
            reverse('products:product_detail', args=[99999])
        )
        self.assertEqual(response.status_code, 404)

    def test_product_detail_available_sizes(self):
        """Test product_detail shows available sizes"""
        ProductSize.objects.create(
            product=self.product,
            size="L",
            quantity=5
        )
        response = self.client.get(
            reverse('products:product_detail', args=[self.product.product_id])
        )
        available_sizes = response.context['available_sizes']
        self.assertIn('L', [s.size for s in available_sizes])

    def test_product_detail_no_available_sizes(self):
        """Test product_detail with no available sizes"""
        ProductSize.objects.create(
            product=self.product,
            size="L",
            quantity=0  # Out of stock
        )
        response = self.client.get(
            reverse('products:product_detail', args=[self.product.product_id])
        )
        available_sizes = response.context['available_sizes']
        self.assertEqual(len(list(available_sizes)), 0)

    def test_product_detail_review_count(self):
        """Test product_detail shows correct review count"""
        # Create approved reviews
        ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            title="Good",
            comment="Good product",
            approved=True
        )
        ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            title="Good",
            comment="Good product",
            approved=True
        )
        # Create unapproved review
        ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=3,
            title="OK",
            comment="OK product",
            approved=False
        )
        response = self.client.get(
            reverse('products:product_detail', args=[self.product.product_id])
        )
        self.assertEqual(response.context['review_count'], 2)

    def test_product_detail_review_form_displayed(self):
        """Test product_detail displays review form"""
        response = self.client.get(
            reverse('products:product_detail', args=[self.product.product_id])
        )
        self.assertIn('review_form', response.context)

    def test_product_detail_post_valid_review(self):
        """Test submitting a valid review"""
        self.client.login(username='testuser', password='pass123')
        response = self.client.post(
            reverse('products:product_detail', args=[self.product.product_id]),
            {
                'rating': 5,
                'title': 'Excellent product',
                'comment': 'Very happy with this purchase!'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            ProductReview.objects.filter(product=self.product).exists()
        )

    def test_product_detail_post_review_not_approved_regular_user(self):
        """Test review from regular user is not auto-approved"""
        self.client.login(username='testuser', password='pass123')
        self.client.post(
            reverse('products:product_detail', args=[self.product.product_id]),
            {
                'rating': 5,
                'title': 'Excellent',
                'comment': 'Great!'
            }
        )
        review = ProductReview.objects.get(product=self.product)
        self.assertFalse(review.approved)

    def test_product_detail_post_review_requires_login(self):
        """Test review submission fails for anonymous users"""
        # Anonymous user cannot submit a review because
        #  user field requires authenticated User
        # This view will raise an error if anonymous user tries to submit
        with self.assertRaises(ValueError):
            self.client.post(
                reverse('products:product_detail',
                        args=[self.product.product_id]),
                {
                    'rating': 5,
                    'title': 'Good',
                    'comment': 'Good product'
                }
            )

    def test_product_detail_product_images(self):
        """Test product_detail includes product images"""
        ProductImage.objects.create(
            product=self.product,
            image="placeholder"
        )
        response = self.client.get(
            reverse('products:product_detail', args=[self.product.product_id])
        )
        self.assertIn('product_images', response.context)


class TestReviewEditView(TestCase):
    """Test review_edit view"""

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Test")
        self.product = Product.objects.create(
            name="Product",
            brand="Brand",
            colour="Red",
            size="M",
            description="Desc",
            price=Decimal("50.00"),
            category=self.category
        )
        self.user = User.objects.create_user(
            username="user1",
            password="pass123",
            email="user1@test.com"
        )
        self.other_user = User.objects.create_user(
            username="user2",
            password="pass123",
            email="user2@test.com"
        )
        self.staff_user = User.objects.create_user(
            username="staff",
            password="pass123",
            email="staff@test.com",
            is_staff=True
        )
        self.review = ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=3,
            title="OK",
            comment="It's okay"
        )

    def test_review_edit_author_can_edit(self):
        """Test author can edit their own review"""
        self.client.login(username='user1', password='pass123')
        response = self.client.post(
            reverse('products:review_edit',
                    args=[self.product.product_id, self.review.review_id]),
            {
                'rating': 4,
                'title': 'Good',
                'comment': 'Actually very good'
            }
        )
        self.assertEqual(response.status_code, 302)
        updated_review = ProductReview.objects.get(pk=self.review.review_id)
        self.assertEqual(updated_review.rating, 4)
        self.assertEqual(updated_review.title, 'Good')

    def test_review_edit_other_user_cannot_edit(self):
        """Test other user cannot edit review"""
        self.client.login(username='user2', password='pass123')
        original_rating = self.review.rating
        self.client.post(
            reverse('products:review_edit',
                    args=[self.product.product_id, self.review.review_id]),
            {
                'rating': 5,
                'title': 'Changed',
                'comment': 'Changed comment'
            }
        )
        updated_review = ProductReview.objects.get(pk=self.review.review_id)
        self.assertEqual(updated_review.rating, original_rating)

    def test_review_edit_staff_can_edit(self):
        """Test staff can edit any review"""
        self.client.login(username='staff', password='pass123')
        self.client.post(
            reverse('products:review_edit',
                    args=[self.product.product_id, self.review.review_id]),
            {
                'rating': 5,
                'title': 'Staff edited',
                'comment': 'Staff comment',
                'approved': True
            }
        )
        updated_review = ProductReview.objects.get(pk=self.review.review_id)
        self.assertEqual(updated_review.rating, 5)
        self.assertEqual(updated_review.title, 'Staff edited')
        self.assertTrue(updated_review.approved)

    def test_review_edit_regular_user_approval_reset(self):
        """Test regular user edit resets approval"""
        self.review.approved = True
        self.review.save()
        self.client.login(username='user1', password='pass123')
        self.client.post(
            reverse('products:review_edit',
                    args=[self.product.product_id, self.review.review_id]),
            {
                'rating': 4,
                'title': 'Updated',
                'comment': 'Updated comment'
            }
        )
        updated_review = ProductReview.objects.get(pk=self.review.review_id)
        self.assertFalse(updated_review.approved)

    def test_review_edit_nonexistent_review(self):
        """Test editing non-existent review"""
        self.client.login(username='user1', password='pass123')
        response = self.client.post(
            reverse('products:review_edit',
                    args=[self.product.product_id, 99999])
        )
        self.assertEqual(response.status_code, 404)


class TestReviewDeleteView(TestCase):
    """Test review_delete view"""

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Test")
        self.product = Product.objects.create(
            name="Product",
            brand="Brand",
            colour="Red",
            size="M",
            description="Desc",
            price=Decimal("50.00"),
            category=self.category
        )
        self.user = User.objects.create_user(
            username="user1",
            password="pass123",
            email="user1@test.com"
        )
        self.other_user = User.objects.create_user(
            username="user2",
            password="pass123",
            email="user2@test.com"
        )
        self.review = ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=3,
            title="OK",
            comment="It's okay"
        )

    def test_review_delete_by_author(self):
        """Test author can delete their review"""
        self.client.login(username='user1', password='pass123')
        review_id = self.review.review_id
        self.client.post(
            reverse('products:review_delete',
                    args=[self.product.product_id, review_id])
        )
        self.assertFalse(
            ProductReview.objects.filter(review_id=review_id).exists()
        )

    def test_review_delete_by_other_user_fails(self):
        """Test other user cannot delete review"""
        self.client.login(username='user2', password='pass123')
        review_id = self.review.review_id
        self.client.post(
            reverse('products:review_delete',
                    args=[self.product.product_id, review_id])
        )
        self.assertTrue(
            ProductReview.objects.filter(review_id=review_id).exists()
        )

    def test_review_delete_nonexistent_review(self):
        """Test deleting non-existent review"""
        self.client.login(username='user1', password='pass123')
        response = self.client.post(
            reverse('products:review_delete',
                    args=[self.product.product_id, 99999])
        )
        self.assertEqual(response.status_code, 404)

    def test_review_delete_requires_login(self):
        """Test delete requires authentication"""
        response = self.client.post(
            reverse('products:review_delete',
                    args=[self.product.product_id, self.review.review_id])
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_create_product_review(self):
        review = ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment="Good quality"
        )
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.user, self.user)
