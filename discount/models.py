from django.db import models
from products.models import Product, Category

# Create your models here.


class ProductDiscount(models.Model):
    """Model representing a discount applied to a product or category by admin without a code."""
    discount_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='discounts',
        null=True,
        blank=True,
        help_text='Null means this code applies to all categories')
    category = models.ForeignKey(
        'products.Category',
        on_delete=models.CASCADE,
        related_name='discount_codes',
        null=True,
        blank=True,
        help_text='Null means this code applies to all categories'
    )
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        max_value=100,
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class DiscountCode(models.Model):
        """Model representing a discount code that can be applied to an order, category, or product by entering a code.
        If category is null, the code applies to all categories.
        """
        code_id = models.AutoField(primary_key=True)
        code = models.CharField(max_length=50, unique=True)
        discount_percentage = models.DecimalField(
            max_digits=5,
            decimal_places=2,
            max_value=100,
        )
        start_date = models.DateTimeField()
        end_date = models.DateTimeField()
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
