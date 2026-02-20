from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db.models import CheckConstraint, constraints


class Product(models.Model):
    """Product model representing an item in the store."""
    product_id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name='products')
    colour = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    image = CloudinaryField('image', default='placeholder')
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand} {self.name} ({self.colour}, {self.size})"


class ProductSize(models.Model):
    """Model to represent available sizes for a product."""
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='available_sizes')
    size = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - Size: {self.size} (Quantity: {self.quantity})"


class ProductReview(models.Model):
    """ProductReview model representing a review for a product.
        Requires approval before being visible to the public."""
    review_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    # In a real app, this would be a ForeignKey to the User model
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='userreviews')
    rating = models.IntegerField()
    title = models.CharField(max_length=255)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']


class ProductImage(models.Model):
    """Model to represent multiple images for a product."""
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image')

    def __str__(self):
        return f"{self.product.name} - Image {self.id}"


class Category(models.Model):
    """Category model representing a product category."""
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['category_id']

    def __str__(self):
        return f"{self.name}"


class ProductDiscount(models.Model):
    """Model representing a discount applied to a product or category by admin without a code."""
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='product_discounts',
        null=True,
        blank=True,
        help_text='Null means this discount applies to all products')
    category = models.ForeignKey(
        'products.Category',
        on_delete=models.CASCADE,
        related_name='category',
        null=True,
        blank=True,
        help_text='Null means this discount applies to all categories'
    )
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            CheckConstraint(
                check=models.Q(discount_percentage__gte=0) & models.Q(
                    discount_percentage__lte=100),
                name="check_product_discount_percentage"
            )
        ]


class DiscountCode(models.Model):
    """Model representing a discount code that can be applied to an order, category, or product by entering a code.
    If category is null, the code applies to all categories.
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    category = models.ForeignKey(
        'products.Category',
        on_delete=models.CASCADE,
        related_name='discount_codes',
        null=True,
        blank=True,
        help_text='Null means this code applies to all categories'
    )
    max_uses = models.PositiveIntegerField(null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            CheckConstraint(
                check=models.Q(discount_percentage__gte=0) & models.Q(
                    discount_percentage__lte=100),
                name="check_code_discount_percentage"
            )
        ]
