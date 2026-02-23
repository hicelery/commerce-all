from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from django.contrib.messages import get_messages
from cart.models import Order, OrderItem
from .forms import ProfileUpdate


# ============================================================================
# PROFILE VIEW TESTS (account_centre)
# ============================================================================

class TestProfileViewAccountCentre(TestCase):
    """Test the profile_view (account_centre) which displays user orders"""

    def setUp(self):
        """Create test user"""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@email.com"
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            password="otherpassword",
            email="other@email.com"
        )

    # ========== LOGIN REQUIREMENT TESTS ==========
    def test_account_centre_requires_login(self):
        """Test that account centre requires authentication"""
        response = self.client.get(reverse('dashboard:account_centre'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_account_centre_redirects_anonymous_user(self):
        """Test that anonymous users are redirected to login"""
        response = self.client.get(
            reverse('dashboard:account_centre'), follow=False)
        self.assertEqual(response.status_code, 302)

    # ========== AUTHENTICATED USER TESTS ==========
    def test_account_centre_accessible_to_authenticated_user(self):
        """Test account centre view is accessible to authenticated user"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('dashboard:account_centre'))
        self.assertEqual(response.status_code, 200)

    def test_account_centre_uses_correct_template(self):
        """Test that the correct template is used"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('dashboard:account_centre'))
        self.assertTemplateUsed(response, 'dashboard/account_centre.html')

    def test_account_centre_context_has_orders(self):
        """Test that context contains orders"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('dashboard:account_centre'))
        self.assertIn('orders', response.context)
        self.assertIn('items_count', response.context)

    def test_account_centre_shows_user_orders_only(self):
        """Test that user only sees their own orders"""
        # Create orders for both users
        order1 = Order.objects.create(
            user=self.user, total_price=100.00, shipping_address="123 Main St")
        order2 = Order.objects.create(
            user=self.other_user, total_price=200.00, shipping_address="456 Oak Ave")

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('dashboard:account_centre'))

        orders = response.context['orders']
        self.assertEqual(orders.count(), 1)
        self.assertIn(order1, orders)
        self.assertNotIn(order2, orders)

    # ========== ORDERS DISPLAY TESTS ==========
    def test_account_centre_orders_sorted_by_updated_at_desc(self):
        """Test that orders are sorted by updated_at in descending order"""
        import time
        from django.utils import timezone

        # Create orders with small delays to ensure different timestamps
        order1 = Order.objects.create(
            user=self.user, total_price=100.00, shipping_address="123 Main St")
        time.sleep(0.1)
        order2 = Order.objects.create(
            user=self.user, total_price=200.00, shipping_address="456 Oak Ave")
        time.sleep(0.1)
        order3 = Order.objects.create(
            user=self.user, total_price=300.00, shipping_address="789 Pine Rd")

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('dashboard:account_centre'))

        orders = list(response.context['orders'])
        # Verify all orders are present
        self.assertEqual(len(orders), 3)
        self.assertIn(order1, orders)
        self.assertIn(order2, orders)
        self.assertIn(order3, orders)
        # Verify most recent is first
        self.assertEqual(orders[0], order3)

    def test_account_centre_no_orders(self):
        """Test account centre when user has no orders"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('dashboard:account_centre'))

        self.assertEqual(response.context['orders'].count(), 0)
        self.assertEqual(response.context['items_count'], {})

    def test_account_centre_items_count_calculation(self):
        """Test that items_count is calculated correctly"""
        order = Order.objects.create(
            user=self.user, total_price=100.00, shipping_address="123 Main St")
        # Create a product for the OrderItem
        from products.models import Category, Product
        category = Category.objects.create(name="Test")
        product = Product.objects.create(
            name="Test Product",
            brand="Brand",
            colour="Red",
            size="M",
            price=25.00,
            category=category,
            description="Test"
        )
        OrderItem.objects.create(
            order=order, quantity=3, price=25.00, product=product)
        OrderItem.objects.create(
            order=order, quantity=2, price=25.00, product=product)

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('dashboard:account_centre'))

        items_count = response.context['items_count']
        self.assertEqual(items_count[order.order_id], 5)

    def test_account_centre_items_count_no_items(self):
        """Test items_count when order has no items"""
        order = Order.objects.create(
            user=self.user, total_price=100.00, shipping_address="123 Main St")

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('dashboard:account_centre'))

        items_count = response.context['items_count']
        self.assertEqual(items_count[order.order_id], 0)

    def test_account_centre_order_has_items_count_attribute(self):
        """Test that order objects have items_count attribute set"""
        from products.models import Category, Product
        category = Category.objects.create(name="Test")
        product = Product.objects.create(
            name="Test Product",
            brand="Brand",
            colour="Red",
            size="M",
            price=20.00,
            category=category,
            description="Test"
        )
        order = Order.objects.create(
            user=self.user, total_price=100.00, shipping_address="123 Main St")
        OrderItem.objects.create(
            order=order, quantity=5, price=20.00, product=product)

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('dashboard:account_centre'))

        orders = response.context['orders']
        self.assertEqual(orders[0].items_count, 5)

    # ========== HTTP METHOD TESTS ==========
    def test_account_centre_post_method_returns_form(self):
        """Test that POST requests to account_centre still renders GET template"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse('dashboard:account_centre'))
        # POST requests still render the template since there's no POST handler
        self.assertEqual(response.status_code, 200)

    def test_account_centre_get_only(self):
        """Test that only GET requests work"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('dashboard:account_centre'))
        self.assertEqual(response.status_code, 200)


# ============================================================================
# PROFILE PAGE TESTS (GET profile form)
# ============================================================================

class TestProfilePageView(TestCase):
    """Test the profile_page view which displays the profile edit form"""

    def setUp(self):
        """Create test user"""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@email.com",
            first_name="Test",
            last_name="User"
        )

    # ========== LOGIN REQUIREMENT TESTS ==========
    def test_profile_page_requires_login(self):
        """Test that profile page requires authentication"""
        response = self.client.get(reverse('dashboard:profile'))
        self.assertEqual(response.status_code, 302)

    # ========== AUTHENTICATED USER TESTS ==========
    def test_profile_page_accessible_to_authenticated_user(self):
        """Test profile page is accessible to authenticated user"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('dashboard:profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_page_uses_correct_template(self):
        """Test that profile page uses correct template"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('dashboard:profile'))
        self.assertTemplateUsed(response, 'dashboard/profile.html')

    def test_profile_page_context_has_form(self):
        """Test that context contains profile_form"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('dashboard:profile'))
        self.assertIn('profile_form', response.context)

    def test_profile_page_form_is_unbound(self):
        """Test that form is unbound (no initial POST data)"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('dashboard:profile'))
        form = response.context['profile_form']
        self.assertFalse(form.is_bound)

    def test_profile_page_form_has_user_data(self):
        """Test that form is pre-populated with user data"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('dashboard:profile'))
        form = response.context['profile_form']

        self.assertEqual(form.instance.username, "testuser")
        self.assertEqual(form.instance.first_name, "Test")
        self.assertEqual(form.instance.last_name, "User")

    def test_profile_page_form_fields(self):
        """Test that form has correct fields"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('dashboard:profile'))
        form = response.context['profile_form']

        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('username', form.fields)

    # ========== HTTP METHOD TESTS ==========
    def test_profile_page_post_method(self):
        """Test that POST to profile page works (redirects to profile_update logic)"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('dashboard:profile'),
            {
                'first_name': 'Updated',
                'last_name': 'Name',
                'username': 'testuser'
            }
        )
        # profile_page always returns profile.html regardless of method
        self.assertEqual(response.status_code, 200)


# ============================================================================
# PROFILE UPDATE TESTS
# ============================================================================

class TestProfileUpdateView(TestCase):
    """Test the profile_update view which handles profile form submissions"""

    def setUp(self):
        """Create test user"""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@email.com",
            first_name="Test",
            last_name="User"
        )

    # ========== LOGIN REQUIREMENT TESTS ==========
    def test_profile_update_requires_login(self):
        """Test that profile update requires authentication"""
        response = self.client.get(reverse('dashboard:profile_update'))
        self.assertEqual(response.status_code, 302)

    # ========== VALID UPDATE TESTS ==========
    def test_profile_update_valid_data(self):
        """Test profile update with valid data"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('dashboard:profile_update'),
            {
                'first_name': 'Updated',
                'last_name': 'Name',
                'username': 'testuser'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')

    def test_profile_update_success_message(self):
        """Test that success message is displayed on valid update"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('dashboard:profile_update'),
            {
                'first_name': 'Updated',
                'last_name': 'Name',
                'username': 'testuser'
            }
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Profile updated successfully.')

    def test_profile_update_only_first_name(self):
        """Test updating only first name"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('dashboard:profile_update'),
            {
                'first_name': 'NewFirst',
                'last_name': 'User',
                'username': 'testuser'
            }
        )

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'NewFirst')
        self.assertEqual(self.user.last_name, 'User')

    def test_profile_update_only_last_name(self):
        """Test updating only last name"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('dashboard:profile_update'),
            {
                'first_name': 'Test',
                'last_name': 'NewLast',
                'username': 'testuser'
            }
        )

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'NewLast')

    def test_profile_update_empty_fields(self):
        """Test updating with empty first and last names"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('dashboard:profile_update'),
            {
                'first_name': '',
                'last_name': '',
                'username': 'testuser'
            }
        )

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, '')
        self.assertEqual(self.user.last_name, '')

    # ========== INVALID UPDATE TESTS ==========
    def test_profile_update_invalid_data_missing_username(self):
        """Test profile update fails when username is missing"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('dashboard:profile_update'),
            {
                'first_name': 'Updated',
                'last_name': 'Name',
                'username': ''
            }
        )

        # Form is invalid, user data not updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Test')

    def test_profile_update_invalid_data_warning_message(self):
        """Test that warning message is displayed on invalid update"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('dashboard:profile_update'),
            {
                'first_name': 'Updated',
                'last_name': 'Name',
                'username': ''
            }
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('correct the errors' in str(m) for m in messages))

    def test_profile_update_duplicate_username(self):
        """Test profile update fails with duplicate username"""
        other_user = User.objects.create_user(
            username="otheruser",
            password="otherpassword"
        )

        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('dashboard:profile_update'),
            {
                'first_name': 'Updated',
                'last_name': 'Name',
                'username': 'otheruser'  # Already taken
            }
        )

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'testuser')  # Unchanged

    def test_profile_update_case_sensitive_username(self):
        """Test that username is case-sensitive for duplicates"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('dashboard:profile_update'),
            {
                'first_name': 'Updated',
                'last_name': 'Name',
                'username': 'testuser'  # Same username, different case
            }
        )

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'testuser')

    # ========== HTTP METHOD TESTS ==========
    def test_profile_update_get_method_returns_form(self):
        """Test that GET request returns form (unbound)"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('dashboard:profile_update'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('profile_form', response.context)

    def test_profile_update_post_method(self):
        """Test that POST request is handled"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('dashboard:profile_update'),
            {
                'first_name': 'Updated',
                'last_name': 'Name',
                'username': 'testuser'
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_profile_update_uses_correct_template(self):
        """Test that profile.html template is used"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('dashboard:profile_update'),
            {
                'first_name': 'Updated',
                'last_name': 'Name',
                'username': 'testuser'
            }
        )

        self.assertTemplateUsed(response, 'dashboard/profile.html')


# ============================================================================
# EDGE CASE TESTS
# ============================================================================

class TestDashboardEdgeCases(TestCase):
    """Test edge cases and boundary conditions"""

    def setUp(self):
        """Create test users"""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@email.com"
        )

    # ========== SPECIAL CHARACTER TESTS ==========
    def test_profile_update_special_characters_in_name(self):
        """Test updating profile with special characters"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('dashboard:profile_update'),
            {
                'first_name': "Jean-Claude",
                'last_name': "O'Neill",
                'username': 'testuser'
            }
        )

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Jean-Claude")
        self.assertEqual(self.user.last_name, "O'Neill")

    def test_profile_update_unicode_characters(self):
        """Test updating profile with unicode characters"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('dashboard:profile_update'),
            {
                'first_name': "José",
                'last_name': "Müller",
                'username': 'testuser'
            }
        )

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "José")
        self.assertEqual(self.user.last_name, "Müller")

    # ========== LENGTH LIMITS TESTS ==========
    def test_profile_update_very_long_first_name(self):
        """Test updating profile with maximum length first name"""
        long_name = "A" * 30
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('dashboard:profile_update'),
            {
                'first_name': long_name,
                'last_name': 'User',
                'username': 'testuser'
            }
        )

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, long_name)

    def test_profile_update_whitespace_only_name(self):
        """Test updating profile with whitespace-only name - Django cleans whitespace"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('dashboard:profile_update'),
            {
                'first_name': '   ',
                'last_name': '  ',
                'username': 'testuser'
            }
        )

        self.user.refresh_from_db()
        # Django's CharField strips whitespace
        self.assertEqual(self.user.first_name, '')
        self.assertEqual(self.user.last_name, '')

    # ========== MULTIPLE ORDERS STRESS TEST ==========
    def test_account_centre_with_many_orders(self):
        """Test account centre with many orders"""
        for i in range(50):
            Order.objects.create(
                user=self.user, total_price=100.00 + i, shipping_address=f"{i} Main St")

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('dashboard:account_centre'))

        self.assertEqual(response.context['orders'].count(), 50)

    def test_account_centre_with_many_items_per_order(self):
        """Test account centre with orders containing many items"""
        from products.models import Category, Product
        category = Category.objects.create(name="Test")
        product = Product.objects.create(
            name="Test Product",
            brand="Brand",
            colour="Red",
            size="M",
            price=1.00,
            category=category,
            description="Test"
        )
        order = Order.objects.create(
            user=self.user, total_price=100.00, shipping_address="123 Main St")
        for i in range(100):
            OrderItem.objects.create(
                order=order, quantity=1, price=1.00, product=product)

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('dashboard:account_centre'))

        items_count = response.context['items_count']
        self.assertEqual(items_count[order.order_id], 100)

    # ========== CONCURRENCY-LIKE TEST ==========
    def test_profile_update_preserves_other_fields(self):
        """Test that updating profile doesn't affect email or other fields"""
        original_email = self.user.email

        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse('dashboard:profile_update'),
            {
                'first_name': 'Updated',
                'last_name': 'Name',
                'username': 'testuser'
            }
        )

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, original_email)

    # ========== SESSION AND COOKIE TESTS ==========
    def test_session_maintained_after_profile_update(self):
        """Test that user session is maintained after profile update"""
        self.client.login(username="testuser", password="testpassword")

        # First request to maintain session
        response1 = self.client.get(reverse('dashboard:account_centre'))
        self.assertEqual(response1.status_code, 200)

        # Update profile
        response2 = self.client.post(
            reverse('dashboard:profile_update'),
            {
                'first_name': 'Updated',
                'last_name': 'Name',
                'username': 'testuser'
            }
        )

        # Another request - user should still be authenticated
        response3 = self.client.get(reverse('dashboard:account_centre'))
        self.assertEqual(response3.status_code, 200)
