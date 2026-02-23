from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product, Category, DiscountCode
from datetime import datetime, timedelta


class TestCartModel(TestCase):
    """Tests for Cart model"""

    def setUp(self):
        """Create test data"""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    # ========== BASIC CREATION TESTS ==========
    def test_cart_creation_anonymous(self):
        """Test creating anonymous cart without user"""
        cart = Cart.objects.create(is_active=True)
        self.assertTrue(cart.pk)
        self.assertIsNone(cart.user)
        self.assertTrue(cart.is_active)

    def test_cart_creation_authenticated(self):
        """Test creating cart for authenticated user"""
        cart = Cart.objects.create(user=self.user, is_active=True)
        self.assertEqual(cart.user, self.user)
        self.assertTrue(cart.is_active)

    def test_cart_string_representation(self):
        """Test cart model string output"""
        cart = Cart.objects.create(user=self.user)
        # Cart has a default __str__ or model name will be used
        self.assertTrue(str(cart))

    # ========== TIMESTAMPS TESTS ==========
    def test_cart_created_at_timestamp(self):
        """Test that created_at timestamp is set"""
        cart = Cart.objects.create(user=self.user)
        self.assertIsNotNone(cart.created_at)

    def test_cart_updated_at_timestamp(self):
        """Test that updated_at timestamp is set"""
        cart = Cart.objects.create(user=self.user)
        self.assertIsNotNone(cart.updated_at)

    # ========== STATUS TESTS ==========
    def test_cart_is_active_default(self):
        """Test that is_active defaults to True"""
        cart = Cart.objects.create(user=self.user)
        self.assertTrue(cart.is_active)

    def test_cart_is_active_false(self):
        """Test creating inactive cart"""
        cart = Cart.objects.create(user=self.user, is_active=False)
        self.assertFalse(cart.is_active)

    # ========== RELATIONSHIPS TESTS ==========
    def test_cart_related_items(self):
        """Test that cart can have multiple items"""
        cart = Cart.objects.create(user=self.user)
        category = Category.objects.create(name="Test")
        product1 = Product.objects.create(
            name="Product 1", brand="B", colour="Red", size="M",
            price=10.00, category=category, description="Test"
        )
        product2 = Product.objects.create(
            name="Product 2", brand="B", colour="Blue", size="L",
            price=20.00, category=category, description="Test"
        )
        CartItem.objects.create(cart=cart, product=product1, quantity=1)
        CartItem.objects.create(cart=cart, product=product2, quantity=2)

        self.assertEqual(cart.items.count(), 2)

    # ========== MULTIPLE CARTS FOR USER TESTS ==========
    def test_multiple_carts_same_user(self):
        """Test that user can have multiple carts"""
        cart1 = Cart.objects.create(user=self.user, is_active=True)
        cart2 = Cart.objects.create(user=self.user, is_active=False)

        user_carts = Cart.objects.filter(user=self.user)
        self.assertEqual(user_carts.count(), 2)


class TestCartItemModel(TestCase):
    """Tests for CartItem model"""

    def setUp(self):
        """Create test data"""
        self.user = User.objects.create_user(username="testuser")
        self.cart = Cart.objects.create(user=self.user)
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

    # ========== BASIC CREATION TESTS ==========
    def test_cartitem_creation(self):
        """Test creating cart item"""
        item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.product, self.product)

    def test_cartitem_with_size(self):
        """Test creating cart item with size"""
        item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=1,
            size="L"
        )
        self.assertEqual(item.size, "L")

    def test_cartitem_default_quantity(self):
        """Test cart item default quantity is 1"""
        item = CartItem.objects.create(cart=self.cart, product=self.product)
        self.assertEqual(item.quantity, 1)

    # ========== TIMESTAMPS TESTS ==========
    def test_cartitem_created_at(self):
        """Test cart item has created_at timestamp"""
        item = CartItem.objects.create(cart=self.cart, product=self.product)
        self.assertIsNotNone(item.created_at)

    def test_cartitem_updated_at(self):
        """Test cart item has updated_at timestamp"""
        item = CartItem.objects.create(cart=self.cart, product=self.product)
        self.assertIsNotNone(item.updated_at)

    # ========== QUANTITY TESTS ==========
    def test_cartitem_quantity_increment(self):
        """Test incrementing cart item quantity"""
        item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )
        item.quantity += 3
        item.save()
        item.refresh_from_db()
        self.assertEqual(item.quantity, 5)

    def test_cartitem_quantity_zero(self):
        """Test cart item with zero quantity"""
        item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=0
        )
        self.assertEqual(item.quantity, 0)

    # ========== RELATIONSHIP TESTS ==========
    def test_cartitem_belongs_to_cart(self):
        """Test cart item belongs to correct cart"""
        item = CartItem.objects.create(
            cart=self.cart,
            product=self.product
        )
        self.assertEqual(item.cart, self.cart)

    def test_cartitem_references_product(self):
        """Test cart item references correct product"""
        item = CartItem.objects.create(
            cart=self.cart,
            product=self.product
        )
        self.assertEqual(item.product, self.product)

    # ========== MULTIPLE ITEMS TESTS ==========
    def test_same_product_different_sizes(self):
        """Test cart can have same product with different sizes"""
        item1 = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=1,
            size="M"
        )
        item2 = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=1,
            size="L"
        )

        items = CartItem.objects.filter(cart=self.cart, product=self.product)
        self.assertEqual(items.count(), 2)


class TestOrderModel(TestCase):
    """Tests for Order model"""

    def setUp(self):
        """Create test data"""
        self.user = User.objects.create_user(username="testuser")
        self.cart = Cart.objects.create(user=self.user)
        self.category = Category.objects.create(name="Test")
        self.discount_code = DiscountCode.objects.create(
            code="SAVE10",
            discount_percentage=10,
            start_date=datetime.now() - timedelta(days=1),
            end_date=datetime.now() + timedelta(days=1),
            max_uses=100
        )

    # ========== BASIC CREATION TESTS ==========
    def test_order_creation(self):
        """Test creating an order"""
        order = Order.objects.create(
            user=self.user,
            total_price=100.00,
            shipping_address="123 Main St",
            cart=self.cart
        )
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.total_price, Decimal('100.00'))

    def test_order_without_cart(self):
        """Test creating order without cart"""
        order = Order.objects.create(
            user=self.user,
            total_price=100.00,
            shipping_address="123 Main St"
        )
        self.assertIsNone(order.cart)

    def test_order_with_discount_code(self):
        """Test order with discount code"""
        order = Order.objects.create(
            user=self.user,
            total_price=90.00,
            shipping_address="123 Main St",
            discount_code=self.discount_code
        )
        self.assertEqual(order.discount_code, self.discount_code)

    # ========== STATUS TESTS ==========
    def test_order_is_paid_default(self):
        """Test that is_paid defaults to False"""
        order = Order.objects.create(
            user=self.user,
            total_price=100.00,
            shipping_address="123 Main St"
        )
        self.assertFalse(order.is_paid)

    def test_order_mark_as_paid(self):
        """Test marking order as paid"""
        order = Order.objects.create(
            user=self.user,
            total_price=100.00,
            shipping_address="123 Main St"
        )
        order.is_paid = True
        order.save()
        order.refresh_from_db()
        self.assertTrue(order.is_paid)

    # ========== CONTACT INFORMATION TESTS ==========
    def test_order_with_contact_number(self):
        """Test order with contact number"""
        order = Order.objects.create(
            user=self.user,
            total_price=100.00,
            shipping_address="123 Main St",
            contactno="555-1234"
        )
        self.assertEqual(order.contactno, "555-1234")

    def test_order_contact_number_optional(self):
        """Test that contact number is optional"""
        order = Order.objects.create(
            user=self.user,
            total_price=100.00,
            shipping_address="123 Main St"
        )
        self.assertIsNone(order.contactno)

    # ========== TIMESTAMPS TESTS ==========
    def test_order_created_at(self):
        """Test order has created_at timestamp"""
        order = Order.objects.create(
            user=self.user,
            total_price=100.00,
            shipping_address="123 Main St"
        )
        self.assertIsNotNone(order.created_at)

    def test_order_updated_at(self):
        """Test order has updated_at timestamp"""
        order = Order.objects.create(
            user=self.user,
            total_price=100.00,
            shipping_address="123 Main St"
        )
        self.assertIsNotNone(order.updated_at)

    # ========== RELATIONSHIP TESTS ==========
    def test_order_belongs_to_user(self):
        """Test order belongs to correct user"""
        order = Order.objects.create(
            user=self.user,
            total_price=100.00,
            shipping_address="123 Main St"
        )
        self.assertEqual(order.user, self.user)

    # ========== ORDERING TESTS ==========
    def test_get_unpaid_orders_for_user(self):
        """Test getting unpaid orders for user"""
        order1 = Order.objects.create(
            user=self.user,
            total_price=100.00,
            shipping_address="123 Main St",
            is_paid=False
        )
        order2 = Order.objects.create(
            user=self.user,
            total_price=50.00,
            shipping_address="456 Oak Ave",
            is_paid=True
        )

        unpaid_orders = Order.objects.filter(user=self.user, is_paid=False)
        self.assertEqual(unpaid_orders.count(), 1)
        self.assertEqual(unpaid_orders.first(), order1)


class TestOrderItemModel(TestCase):
    """Tests for OrderItem model"""

    def setUp(self):
        """Create test data"""
        self.user = User.objects.create_user(username="testuser")
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
        self.order = Order.objects.create(
            user=self.user,
            total_price=100.00,
            shipping_address="123 Main St"
        )

    # ========== BASIC CREATION TESTS ==========
    def test_orderitem_creation(self):
        """Test creating order item"""
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=50.00
        )
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.price, Decimal('50.00'))

    def test_orderitem_with_size(self):
        """Test creating order item with size"""
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price=50.00,
            size="L"
        )
        self.assertEqual(item.size, "L")

    # ========== SUBTOTAL PROPERTY TESTS ==========
    def test_orderitem_subtotal_calculation(self):
        """Test order item subtotal calculation"""
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=3,
            price=25.00
        )
        self.assertEqual(item.subtotal, Decimal('75.00'))

    def test_orderitem_subtotal_single_quantity(self):
        """Test subtotal with quantity 1"""
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price=50.00
        )
        self.assertEqual(item.subtotal, Decimal('50.00'))

    def test_orderitem_subtotal_zero_quantity(self):
        """Test subtotal with zero quantity"""
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=0,
            price=50.00
        )
        self.assertEqual(item.subtotal, Decimal('0.00'))

    # ========== RELATIONSHIPS TESTS ==========
    def test_orderitem_belongs_to_order(self):
        """Test order item belongs to correct order"""
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price=50.00
        )
        self.assertEqual(item.order, self.order)

    def test_orderitem_references_product(self):
        """Test order item references correct product"""
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price=50.00
        )
        self.assertEqual(item.product, self.product)

    # ========== TIMESTAMPS TESTS ==========
    def test_orderitem_created_at(self):
        """Test order item has created_at timestamp"""
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price=50.00
        )
        self.assertIsNotNone(item.created_at)

    def test_orderitem_updated_at(self):
        """Test order item has updated_at timestamp"""
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price=50.00
        )
        self.assertIsNotNone(item.updated_at)

    # ========== MULTIPLE ITEMS TESTS ==========
    def test_order_multiple_items(self):
        """Test order can have multiple items"""
        product2 = Product.objects.create(
            name="Product 2",
            brand="Brand",
            colour="Blue",
            size="L",
            price=30.00,
            category=self.category,
            description="Test"
        )
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=50.00
        )
        OrderItem.objects.create(
            order=self.order,
            product=product2,
            quantity=1,
            price=30.00
        )

        items = self.order.items.all()
        self.assertEqual(items.count(), 2)

    # ========== DECIMAL PRECISION TESTS ==========
    def test_orderitem_price_decimal_precision(self):
        """Test that price maintains decimal precision"""
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=3,
            price=Decimal('19.99')
        )
        self.assertEqual(item.price, Decimal('19.99'))
