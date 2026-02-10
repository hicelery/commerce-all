from django.db import models
from django.contrib.auth.models import User

# Create your models here.


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
    image = models.URLField(max_length=500)
    description = models.TextField()
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


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
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']


class Category(models.Model):
    """Category model representing a product category."""
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']
