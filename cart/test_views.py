from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import get_messages
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product, Category, DiscountCode
from datetime import datetime, timedelta
from decimal import Decimal


class TestCartDetailView(TestCase):
    """Tests for cart_detail view"""

    def setUp(self):
        """Create test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="test@test.com"
        )
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            brand="Brand",
            colour="Red",
            size="M",
            price=50.00,
            discounted_price=45.00,
            category=self.category,
            description="Test"
        )

    # ========== ANONYMOUS USER TESTS ==========
    def test_cart_detail_anonymous_user(self):
        """Test cart view for anonymous user"""
        response = self.client.get(reverse('cart:view_cart'))
        self.assertEqual(response.status_code, 200)

    def test_cart_detail_creates_session_cart(self):
        """Test that cart detail creates anonymous cart"""
        response = self.client.get(reverse('cart:view_cart'))
        self.assertIn('cart_id', self.client.session)

    # ========== AUTHENTICATED USER TESTS ==========
    def test_cart_detail_authenticated_user(self):
        """Test cart view for authenticated user"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse('cart:view_cart'))
        self.assertEqual(response.status_code, 200)

    def test_cart_detail_uses_correct_template(self):
        """Test that correct template is used"""
        response = self.client.get(reverse('cart:view_cart'))
        self.assertTemplateUsed(response, 'cart/view_cart.html')

    # ========== CONTEXT TESTS ==========
    def test_cart_detail_context_has_cart(self):
        """Test that context contains cart"""
        response = self.client.get(reverse('cart:view_cart'))
        self.assertIn('cart', response.context)

    def test_cart_detail_context_has_items(self):
        """Test that context contains items list"""
        response = self.client.get(reverse('cart:view_cart'))
        self.assertIn('items', response.context)

    def test_cart_detail_context_has_pricing(self):
        """Test that context contains pricing information"""
        response = self.client.get(reverse('cart:view_cart'))
        self.assertIn('subtotal', response.context)
        self.assertIn('shipping', response.context)
        self.assertIn('total', response.context)

    # ========== EMPTY CART TESTS ==========
    def test_cart_detail_empty_cart(self):
        """Test cart view with empty cart"""
        response = self.client.get(reverse('cart:view_cart'))
        self.assertEqual(response.context['items_count'], 0)

    def test_cart_detail_empty_cart_pricing(self):
        """Test pricing for empty cart"""
        response = self.client.get(reverse('cart:view_cart'))
        self.assertEqual(response.context['subtotal'], 0)

    # ========== SHIPPING COST TESTS ==========
    def test_cart_detail_shipping_free_over_50(self):
        """Test that shipping is free for orders over £50"""
        # Initialize session first by making a GET request
        self.client.get(reverse('cart:view_cart'))

        # Now create our cart and add items to it
        cart = Cart.objects.create(user=self.user, is_active=True)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)

        # Set the session to use our cart
        session = self.client.session
        session['cart_id'] = cart.pk
        session.save()

        # Now make the test request with the correct cart_id in session
        response = self.client.get(reverse('cart:view_cart'))
        # Subtotal should be 90 (2 * 45.00), shipping should be 0
        self.assertEqual(
            Decimal(response.context['subtotal']), Decimal('90.00'))
        self.assertEqual(response.context['shipping'], Decimal('0.00'))

    def test_cart_detail_shipping_charged_under_50(self):
        """Test that shipping is charged for orders under £50"""
        # Initialize session first by making a GET request
        self.client.get(reverse('cart:view_cart'))

        # Create cart and items
        cart = Cart.objects.create(user=self.user, is_active=True)
        product = Product.objects.create(
            name="Cheap Product",
            brand="Brand",
            colour="Blue",
            size="S",
            price=20.00,
            discounted_price=15.00,
            category=self.category,
            description="Test"
        )
        CartItem.objects.create(cart=cart, product=product, quantity=1)

        # Set the session to use our cart
        session = self.client.session
        session['cart_id'] = cart.pk
        session.save()

        response = self.client.get(reverse('cart:view_cart'))
        self.assertEqual(response.context['shipping'], Decimal('9.99'))


class TestAddToCartView(TestCase):
    """Tests for add_to_cart view"""

    def setUp(self):
        """Create test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.category = Category.objects.create(name="Test")
        self.product = Product.objects.create(
            name="Test Product",
            brand="Brand",
            colour="Red",
            size="M",
            price=50.00,
            discounted_price=45.00,
            category=self.category,
            description="Test"
        )

    # ========== BASIC FUNCTIONALITY TESTS ==========
    def test_add_to_cart_anonymous_user(self):
        """Test adding product to cart as anonymous user"""
        response = self.client.post(
            reverse('cart:add_to_cart', args=[self.product.pk]),
            {'quantity': 1}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CartItem.objects.exists())

    def test_add_to_cart_authenticated_user(self):
        """Test adding product to cart as authenticated user"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse('cart:add_to_cart', args=[self.product.pk]),
            {'quantity': 1}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CartItem.objects.exists())

    def test_add_to_cart_increases_quantity(self):
        """Test adding same product twice increases quantity"""
        self.client.post(
            reverse('cart:add_to_cart', args=[self.product.pk]),
            {'quantity': 2}
        )
        self.client.post(
            reverse('cart:add_to_cart', args=[self.product.pk]),
            {'quantity': 3}
        )

        # Should have one item with quantity 5 (2 + 3)
        cart_items = CartItem.objects.filter(product=self.product)
        self.assertEqual(cart_items.count(), 1)
        self.assertEqual(cart_items.first().quantity, 5)

    # ========== QUANTITY TESTS ==========
    def test_add_to_cart_default_quantity(self):
        """Test adding product with default quantity"""
        response = self.client.post(
            reverse('cart:add_to_cart', args=[self.product.pk]),
            {}
        )
        cart_item = CartItem.objects.first()
        self.assertEqual(cart_item.quantity, 1)

    def test_add_to_cart_custom_quantity(self):
        """Test adding product with custom quantity"""
        response = self.client.post(
            reverse('cart:add_to_cart', args=[self.product.pk]),
            {'quantity': 5}
        )
        cart_item = CartItem.objects.first()
        self.assertEqual(cart_item.quantity, 5)

    # ========== SIZE TESTS ==========
    def test_add_to_cart_with_size(self):
        """Test adding product with size"""
        response = self.client.post(
            reverse('cart:add_to_cart', args=[self.product.pk]),
            {'quantity': 1, 'size': 'L'}
        )
        cart_item = CartItem.objects.first()
        self.assertEqual(cart_item.size, 'L')

    def test_add_to_cart_different_sizes_separate_items(self):
        """Test that different sizes create separate cart items"""
        self.client.post(
            reverse('cart:add_to_cart', args=[self.product.pk]),
            {'quantity': 1, 'size': 'M'}
        )
        self.client.post(
            reverse('cart:add_to_cart', args=[self.product.pk]),
            {'quantity': 1, 'size': 'L'}
        )

        items = CartItem.objects.filter(product=self.product)
        self.assertEqual(items.count(), 2)
        sizes = {item.size for item in items}
        self.assertEqual(sizes, {'M', 'L'})

    # ========== INVALID PRODUCT TESTS ==========
    def test_add_to_cart_nonexistent_product(self):
        """Test adding nonexistent product returns 404"""
        response = self.client.post(
            reverse('cart:add_to_cart', args=[9999]),
            {'quantity': 1}
        )
        self.assertEqual(response.status_code, 404)

    # ========== SUCCESS MESSAGES ==========
    def test_add_to_cart_success_message(self):
        """Test success message is displayed"""
        response = self.client.post(
            reverse('cart:add_to_cart', args=[self.product.pk]),
            {'quantity': 1}
        )
        # Check that redirect is successful
        self.assertEqual(response.status_code, 302)
        # Verify item was added
        self.assertTrue(CartItem.objects.exists())


class TestRemoveFromCartView(TestCase):
    """Tests for remove_from_cart view"""

    def setUp(self):
        """Create test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.category = Category.objects.create(name="Test")
        self.product = Product.objects.create(
            name="Test Product",
            brand="Brand",
            colour="Red",
            size="M",
            price=50.00,
            category=self.category,
            description="Test"
        )
        self.cart = Cart.objects.create(user=self.user, is_active=True)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )

    def test_remove_from_cart(self):
        """Test removing item from cart"""
        response = self.client.post(
            reverse('cart:remove_from_cart',
                    args=[self.cart.pk, self.cart_item.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CartItem.objects.filter(
            pk=self.cart_item.pk).exists())

    def test_remove_from_cart_success_message(self):
        """Test success message when item removed"""
        response = self.client.post(
            reverse('cart:remove_from_cart',
                    args=[self.cart.pk, self.cart_item.pk]),
            follow=True
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('removed' in str(m) for m in messages))

    def test_remove_nonexistent_item(self):
        """Test removing nonexistent item returns 404"""
        response = self.client.post(
            reverse('cart:remove_from_cart',
                    args=[self.cart.pk, 9999])
        )
        self.assertEqual(response.status_code, 404)


class TestUpdateCartItemView(TestCase):
    """Tests for update_cart_item view"""

    def setUp(self):
        """Create test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.category = Category.objects.create(name="Test")
        self.product = Product.objects.create(
            name="Test Product",
            brand="Brand",
            colour="Red",
            size="M",
            price=50.00,
            quantity=100,
            category=self.category,
            description="Test",
            discounted_price=45.00
        )
        self.cart = Cart.objects.create(user=self.user, is_active=True)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )

    def test_update_cart_item_increase(self):
        """Test increasing cart item quantity"""
        # The view uses max(quantity + 1, product.quantity) which caps at product.quantity
        response = self.client.post(
            reverse('cart:update_cart_item',
                    args=[self.cart.pk, self.cart_item.pk]),
            {'action': 'increase'}
        )
        self.cart_item.refresh_from_db()
        # Quantity becomes max(2+1, 100) = 100
        self.assertEqual(self.cart_item.quantity, 100)

    def test_update_cart_item_decrease(self):
        """Test decreasing cart item quantity"""
        response = self.client.post(
            reverse('cart:update_cart_item',
                    args=[self.cart.pk, self.cart_item.pk]),
            {'action': 'decrease'}
        )
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 1)

    def test_update_cart_item_decrease_minimum(self):
        """Test that quantity can't go below 1"""
        self.cart_item.quantity = 1
        self.cart_item.save()

        response = self.client.post(
            reverse('cart:update_cart_item',
                    args=[self.cart.pk, self.cart_item.pk]),
            {'action': 'decrease'}
        )
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 1)

    def test_update_cart_item_explicit_quantity(self):
        """Test updating cart item with explicit quantity"""
        response = self.client.post(
            reverse('cart:update_cart_item',
                    args=[self.cart.pk, self.cart_item.pk]),
            {'quantity': 5}
        )
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 5)

    def test_update_cart_item_success_message(self):
        """Test success message when cart updated"""
        response = self.client.post(
            reverse('cart:update_cart_item',
                    args=[self.cart.pk, self.cart_item.pk]),
            {'action': 'increase'},
            follow=True
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('updated' in str(m) for m in messages))


class TestClearCartView(TestCase):
    """Tests for clear_cart view"""

    def setUp(self):
        """Create test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.category = Category.objects.create(name="Test")
        self.product = Product.objects.create(
            name="Test Product",
            brand="Brand",
            colour="Red",
            size="M",
            price=50.00,
            category=self.category,
            description="Test"
        )
        self.cart = Cart.objects.create(user=self.user, is_active=True)
        CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )

    def test_clear_cart(self):
        """Test clearing all items from cart"""
        # Ensure session is initialized by making a GET request first
        self.client.get(reverse('cart:view_cart'))
        # Now set the cart_id in the session that was created
        session = self.client.session
        session['cart_id'] = self.cart.pk
        session.save()

        response = self.client.post(reverse('cart:clear_cart'), follow=True)
        self.assertEqual(CartItem.objects.filter(cart=self.cart).count(), 0)

    def test_clear_cart_success_message(self):
        """Test success message when cart cleared"""
        # Ensure session is initialized by making a GET request first
        self.client.get(reverse('cart:view_cart'))
        # Now set the cart_id in the session that was created
        session = self.client.session
        session['cart_id'] = self.cart.pk
        session.save()

        response = self.client.post(reverse('cart:clear_cart'), follow=True)
        # Verify the cart is cleared
        self.assertEqual(CartItem.objects.filter(cart=self.cart).count(), 0)


class TestApplyDiscountView(TestCase):
    """Tests for apply_discount view"""

    def setUp(self):
        """Create test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.category = Category.objects.create(name="Test")
        self.discount_code = DiscountCode.objects.create(
            code="SAVE10",
            discount_percentage=10,
            start_date=datetime.now() - timedelta(days=1),
            end_date=datetime.now() + timedelta(days=1),
            max_uses=100
        )

    def test_apply_valid_discount_code(self):
        """Test applying valid discount code"""
        response = self.client.post(
            reverse('cart:apply_discount'),
            {'code': 'SAVE10'},
            follow=True
        )
        self.assertIn('applied_discount_code_id', self.client.session)

    def test_apply_invalid_discount_code(self):
        """Test applying invalid discount code"""
        response = self.client.post(
            reverse('cart:apply_discount'),
            {'code': 'INVALID'},
            follow=True
        )
        # When invalid code is applied, session should not contain applied_discount_code_id
        self.assertNotIn('applied_discount_code_id', self.client.session)

    def test_apply_empty_discount_code(self):
        """Test applying empty discount code"""
        response = self.client.post(
            reverse('cart:apply_discount'),
            {'code': ''},
            follow=True
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('enter' in str(m).lower() for m in messages))

    def test_clear_discount_code(self):
        """Test clearing applied discount code"""
        self.client.session['applied_discount_code_id'] = self.discount_code.pk
        self.client.session.save()

        response = self.client.post(
            reverse('cart:apply_discount'),
            {'action': 'clear'},
            follow=True
        )
        self.assertNotIn('applied_discount_code_id', self.client.session)


class TestExpressShipping(TestCase):
    """Tests for express shipping functionality"""

    def setUp(self):
        """Create test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="test@test.com"
        )
        self.category = Category.objects.create(name="Test")
        self.product = Product.objects.create(
            name="Test Product",
            brand="Brand",
            colour="Red",
            size="M",
            price=50.00,
            discounted_price=45.00,
            category=self.category,
            description="Test"
        )

    def test_go_to_checkout_shows_both_shipping_options(self):
        """Test that go_to_checkout provides both shipping costs"""
        self.client.login(username="testuser", password="testpass123")

        # Create cart with an item
        response = self.client.get(reverse('cart:view_cart'))
        session = self.client.session
        session['cart_id'] = session.get('cart_id')
        session.save()

        # Add item to cart
        self.client.post(
            reverse('cart:add_to_cart', args=[self.product.pk]),
            {'quantity': 1}
        )

        # Go to checkout
        response = self.client.get(reverse('cart:go-to-checkout'))

        # Should have both shipping costs in context
        self.assertIn('standard_shipping', response.context)
        self.assertIn('express_shipping', response.context)
        self.assertEqual(
            response.context['express_shipping'], Decimal('14.99'))

    def test_standard_shipping_free_over_50(self):
        """Test standard shipping is free for orders over £50"""
        self.client.login(username="testuser", password="testpass123")

        # Create cart with items totaling over £50
        response = self.client.get(reverse('cart:view_cart'))
        session = self.client.session
        session['cart_id'] = session.get('cart_id')
        session.save()

        # Add 2 items (2 * 45.00 = 90.00)
        self.client.post(
            reverse('cart:add_to_cart', args=[self.product.pk]),
            {'quantity': 2}
        )

        response = self.client.get(reverse('cart:go-to-checkout'))
        # Standard shipping should be free for 90.00 subtotal
        self.assertEqual(
            response.context['standard_shipping'], Decimal('0.00'))

    def test_standard_shipping_charged_under_50(self):
        """Test standard shipping costs £9.99 for orders under £50"""
        self.client.login(username="testuser", password="testpass123")

        # Create cheap product
        cheap_product = Product.objects.create(
            name="Cheap Product",
            brand="Brand",
            colour="Blue",
            size="S",
            price=20.00,
            discounted_price=15.00,
            category=self.category,
            description="Test"
        )

        # Get cart
        response = self.client.get(reverse('cart:view_cart'))
        session = self.client.session
        session['cart_id'] = session.get('cart_id')
        session.save()

        # Add 1 cheap item (15.00 < 50)
        self.client.post(
            reverse('cart:add_to_cart', args=[cheap_product.pk]),
            {'quantity': 1}
        )

        response = self.client.get(reverse('cart:go-to-checkout'))
        # Standard shipping should be 9.99 for 15.00 subtotal
        self.assertEqual(
            response.context['standard_shipping'], Decimal('9.99'))

    def test_express_shipping_always_14_99(self):
        """Test express shipping is always £14.99"""
        self.client.login(username="testuser", password="testpass123")

        # Create cart
        response = self.client.get(reverse('cart:view_cart'))
        session = self.client.session
        session['cart_id'] = session.get('cart_id')
        session.save()

        # Add item
        self.client.post(
            reverse('cart:add_to_cart', args=[self.product.pk]),
            {'quantity': 1}
        )

        response = self.client.get(reverse('cart:go-to-checkout'))
        # Express shipping should always be 14.99
        self.assertEqual(
            response.context['express_shipping'], Decimal('14.99'))
