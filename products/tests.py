from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from .models import (
    Product, Category, ProductReview, ProductSize, ProductImage,
    ProductDiscount, DiscountCode
)


class TestCategoryModel(TestCase):
    """Test Category model"""

    def test_category_creation(self):
        """Test that a category can be created"""
        category = Category.objects.create(name="Electronics")
        self.assertEqual(category.name, "Electronics")

    def test_category_string_representation(self):
        """Test category string representation"""
        category = Category.objects.create(name="Clothing")
        self.assertEqual(str(category), "Clothing")

    def test_category_ordering(self):
        """Test categories are ordered by ID"""
        cat1 = Category.objects.create(name="First")
        cat2 = Category.objects.create(name="Second")
        categories = Category.objects.all()
        self.assertEqual(list(categories), [cat1, cat2])


class TestProductModel(TestCase):
    """Test Product model"""

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")

    def test_product_creation(self):
        """Test that a product can be created"""
        product = Product.objects.create(
            name="Test Product",
            brand="Test Brand",
            colour="Red",
            size="M",
            description="Test Description",
            price=Decimal("29.99"),
            category=self.category
        )
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, Decimal("29.99"))
        self.assertEqual(product.brand, "Test Brand")

    def test_product_string_representation(self):
        """Test product string representation"""
        product = Product.objects.create(
            name="Test Product",
            brand="Test Brand",
            colour="Test Colour",
            size="Test Size",
            description="Test Description",
            price=Decimal("29.99"),
            category=self.category
        )
        self.assertEqual(
            str(product), "Test Brand Test Product (Test Colour, Test Size)")

    def test_product_category_relationship(self):
        """Test product-category foreign key relationship"""
        product = Product.objects.create(
            name="Test Product",
            brand="Test Brand",
            colour="Red",
            size="M",
            description="Test Description",
            price=Decimal("29.99"),
            category=self.category
        )
        self.assertEqual(product.category, self.category)
        self.assertIn(product, self.category.products.all())

    def test_product_default_quantity(self):
        """Test product default quantity is 0"""
        product = Product.objects.create(
            name="Test Product",
            brand="Test Brand",
            colour="Red",
            size="M",
            description="Test Description",
            price=Decimal("29.99"),
            category=self.category
        )
        self.assertEqual(product.quantity, 0)

    def test_product_with_positive_quantity(self):
        """Test product can have positive quantity"""
        product = Product.objects.create(
            name="Test Product",
            brand="Test Brand",
            colour="Red",
            size="M",
            description="Test Description",
            price=Decimal("29.99"),
            category=self.category,
            quantity=100
        )
        self.assertEqual(product.quantity, 100)

    def test_product_discounted_price_null_by_default(self):
        """Test that discounted_price is null by default"""
        product = Product.objects.create(
            name="Test Product",
            brand="Test Brand",
            colour="Red",
            size="M",
            description="Test Description",
            price=Decimal("29.99"),
            category=self.category
        )
        self.assertIsNone(product.discounted_price)

    def test_product_with_discounted_price(self):
        """Test product with discounted price"""
        product = Product.objects.create(
            name="Test Product",
            brand="Test Brand",
            colour="Red",
            size="M",
            description="Test Description",
            price=Decimal("100.00"),
            discounted_price=Decimal("75.00"),
            category=self.category
        )
        self.assertEqual(product.discounted_price, Decimal("75.00"))

    def test_product_ordering_by_created_at(self):
        """Test products are ordered by created_at descending"""
        Product.objects.create(
            name="First", brand="Brand", colour="Red", size="M",
            description="Desc", price=Decimal("10.00"), category=self.category
        )
        # Add a small delay to ensure different timestamps
        import time
        time.sleep(0.01)
        Product.objects.create(
            name="Second", brand="Brand", colour="Red", size="M",
            description="Desc", price=Decimal("20.00"), category=self.category
        )
        products = Product.objects.all()
        # Most recent should be first
        self.assertEqual(products[0].name, "Second")
        self.assertEqual(products[1].name, "First")

    def test_product_timestamps(self):
        """Test that created_at and updated_at are set"""
        product = Product.objects.create(
            name="Test Product",
            brand="Test Brand",
            colour="Red",
            size="M",
            description="Test Description",
            price=Decimal("29.99"),
            category=self.category
        )
        self.assertIsNotNone(product.created_at)
        self.assertIsNotNone(product.updated_at)


class TestProductSizeModel(TestCase):
    """Test ProductSize model"""

    def setUp(self):
        self.category = Category.objects.create(name="Clothing")
        self.product = Product.objects.create(
            name="Test Product",
            brand="Brand",
            colour="Red",
            size="M",
            description="Desc",
            price=Decimal("29.99"),
            category=self.category
        )

    def test_product_size_creation(self):
        """Test ProductSize creation"""
        size = ProductSize.objects.create(
            product=self.product,
            size="L",
            quantity=50
        )
        self.assertEqual(size.size, "L")
        self.assertEqual(size.quantity, 50)

    def test_product_size_default_quantity(self):
        """Test ProductSize default quantity is 0"""
        size = ProductSize.objects.create(
            product=self.product,
            size="XL"
        )
        self.assertEqual(size.quantity, 0)

    def test_product_size_string_representation(self):
        """Test ProductSize string representation"""
        size = ProductSize.objects.create(
            product=self.product,
            size="L",
            quantity=50
        )
        self.assertEqual(str(size), "Test Product - Size: L (Quantity: 50)")

    def test_product_size_cascade_delete(self):
        """Test ProductSize is deleted when Product is deleted"""
        size = ProductSize.objects.create(
            product=self.product,
            size="L",
            quantity=50
        )
        size_id = size.id
        self.product.delete()
        self.assertFalse(ProductSize.objects.filter(id=size_id).exists())


class TestProductReviewModel(TestCase):
    """Test ProductReview model"""

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Test Product",
            brand="Brand",
            colour="Red",
            size="M",
            description="Desc",
            price=Decimal("29.99"),
            category=self.category
        )
        self.user = User.objects.create_user(
            username="reviewer",
            password="pass123",
            email="reviewer@test.com"
        )

    def test_product_review_creation(self):
        """Test ProductReview creation"""
        review = ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            title="Great product!",
            comment="Exceeded expectations"
        )
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.title, "Great product!")

    def test_product_review_default_approved_false(self):
        """Test ProductReview is not approved by default"""
        review = ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            title="Good",
            comment="Good product"
        )
        self.assertFalse(review.approved)

    def test_product_review_approved_flag(self):
        """Test ProductReview can be approved"""
        review = ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            title="Great",
            comment="Great",
            approved=True
        )
        self.assertTrue(review.approved)

    def test_product_review_timestamps(self):
        """Test ProductReview has created_at timestamp"""
        review = ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=3,
            title="OK",
            comment="OK"
        )
        self.assertIsNotNone(review.created_at)

    def test_product_review_cascade_delete(self):
        """Test ProductReview is deleted when Product is deleted"""
        review = ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            title="Great",
            comment="Great"
        )
        review_id = review.review_id
        self.product.delete()
        self.assertFalse(ProductReview.objects.filter(
            review_id=review_id).exists())

    def test_product_review_user_cascade_delete(self):
        """Test ProductReview user cascade"""
        review = ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            title="Great",
            comment="Great"
        )
        review_id = review.review_id
        self.user.delete()
        self.assertFalse(ProductReview.objects.filter(
            review_id=review_id).exists())


class TestProductImageModel(TestCase):
    """Test ProductImage model"""

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Test Product",
            brand="Brand",
            colour="Red",
            size="M",
            description="Desc",
            price=Decimal("29.99"),
            category=self.category
        )

    def test_product_image_creation(self):
        """Test ProductImage creation with cloudinary field"""
        image = ProductImage.objects.create(
            product=self.product,
            image="placeholder"
        )
        self.assertEqual(image.product, self.product)

    def test_product_image_cascade_delete(self):
        """Test ProductImage is deleted when Product is deleted"""
        image = ProductImage.objects.create(
            product=self.product,
            image="placeholder"
        )
        image_id = image.id
        self.product.delete()
        self.assertFalse(ProductImage.objects.filter(id=image_id).exists())

    def test_product_image_string_representation(self):
        """Test ProductImage string representation"""
        image = ProductImage.objects.create(
            product=self.product,
            image="placeholder"
        )
        self.assertIn("Test Product", str(image))


class TestProductDiscountModel(TestCase):
    """Test ProductDiscount model"""

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Test Product",
            brand="Brand",
            colour="Red",
            size="M",
            description="Desc",
            price=Decimal("100.00"),
            category=self.category
        )
        self.now = timezone.now()

    def test_product_discount_creation(self):
        """Test ProductDiscount creation"""
        discount = ProductDiscount.objects.create(
            product=self.product,
            category=self.category,
            discount_percentage=Decimal("10.00"),
            start_date=self.now,
            end_date=self.now + timedelta(days=7)
        )
        self.assertEqual(discount.discount_percentage, Decimal("10.00"))

    def test_product_discount_product_specific(self):
        """Test ProductDiscount for specific product"""
        discount = ProductDiscount.objects.create(
            product=self.product,
            category=None,
            discount_percentage=Decimal("15.00"),
            start_date=self.now,
            end_date=self.now + timedelta(days=7)
        )
        self.assertEqual(discount.product, self.product)
        self.assertIsNone(discount.category)

    def test_product_discount_category_specific(self):
        """Test ProductDiscount for specific category"""
        discount = ProductDiscount.objects.create(
            product=None,
            category=self.category,
            discount_percentage=Decimal("20.00"),
            start_date=self.now,
            end_date=self.now + timedelta(days=7)
        )
        self.assertIsNone(discount.product)
        self.assertEqual(discount.category, self.category)

    def test_product_discount_global(self):
        """Test ProductDiscount applies to all products and categories"""
        discount = ProductDiscount.objects.create(
            product=None,
            category=None,
            discount_percentage=Decimal("5.00"),
            start_date=self.now,
            end_date=self.now + timedelta(days=7)
        )
        self.assertIsNone(discount.product)
        self.assertIsNone(discount.category)

    def test_product_discount_zero_percentage(self):
        """Test ProductDiscount with 0% discount"""
        discount = ProductDiscount.objects.create(
            product=self.product,
            discount_percentage=Decimal("0.00"),
            start_date=self.now,
            end_date=self.now + timedelta(days=7)
        )
        self.assertEqual(discount.discount_percentage, Decimal("0.00"))

    def test_product_discount_hundred_percent(self):
        """Test ProductDiscount with 100% discount"""
        discount = ProductDiscount.objects.create(
            product=self.product,
            discount_percentage=Decimal("100.00"),
            start_date=self.now,
            end_date=self.now + timedelta(days=7)
        )
        self.assertEqual(discount.discount_percentage, Decimal("100.00"))

    def test_product_discount_decimal_percentage(self):
        """Test ProductDiscount with decimal percentage"""
        discount = ProductDiscount.objects.create(
            product=self.product,
            discount_percentage=Decimal("12.50"),
            start_date=self.now,
            end_date=self.now + timedelta(days=7)
        )
        self.assertEqual(discount.discount_percentage, Decimal("12.50"))


class TestDiscountCodeModel(TestCase):
    """Test DiscountCode model"""

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.now = timezone.now()

    def test_discount_code_creation(self):
        """Test DiscountCode creation"""
        code = DiscountCode.objects.create(
            code="SAVE10",
            discount_percentage=Decimal("10.00"),
            category=self.category,
            start_date=self.now,
            end_date=self.now + timedelta(days=7)
        )
        self.assertEqual(code.code, "SAVE10")
        self.assertEqual(code.discount_percentage, Decimal("10.00"))

    def test_discount_code_unique(self):
        """Test discount code must be unique"""
        DiscountCode.objects.create(
            code="UNIQUE",
            discount_percentage=Decimal("10.00"),
            start_date=self.now,
            end_date=self.now + timedelta(days=7)
        )
        with self.assertRaises(Exception):
            DiscountCode.objects.create(
                code="UNIQUE",
                discount_percentage=Decimal("20.00"),
                start_date=self.now,
                end_date=self.now + timedelta(days=7)
            )

    def test_discount_code_no_category(self):
        """Test DiscountCode applies to all categories when category is null"""
        code = DiscountCode.objects.create(
            code="GLOBAL",
            discount_percentage=Decimal("5.00"),
            category=None,
            start_date=self.now,
            end_date=self.now + timedelta(days=7)
        )
        self.assertIsNone(code.category)

    def test_discount_code_max_uses(self):
        """Test DiscountCode max_uses field"""
        code = DiscountCode.objects.create(
            code="LIMITED",
            discount_percentage=Decimal("20.00"),
            max_uses=100,
            start_date=self.now,
            end_date=self.now + timedelta(days=7)
        )
        self.assertEqual(code.max_uses, 100)

    def test_discount_code_no_max_uses(self):
        """Test DiscountCode with no max use limit"""
        code = DiscountCode.objects.create(
            code="UNLIMITED",
            discount_percentage=Decimal("15.00"),
            max_uses=None,
            start_date=self.now,
            end_date=self.now + timedelta(days=7)
        )
        self.assertIsNone(code.max_uses)

    def test_discount_code_zero_percentage(self):
        """Test DiscountCode with 0% discount"""
        code = DiscountCode.objects.create(
            code="ZERO",
            discount_percentage=Decimal("0.00"),
            start_date=self.now,
            end_date=self.now + timedelta(days=7)
        )
        self.assertEqual(code.discount_percentage, Decimal("0.00"))

    def test_discount_code_hundred_percent(self):
        """Test DiscountCode with 100% discount"""
        code = DiscountCode.objects.create(
            code="FREE",
            discount_percentage=Decimal("100.00"),
            start_date=self.now,
            end_date=self.now + timedelta(days=7)
        )
        self.assertEqual(code.discount_percentage, Decimal("100.00"))
