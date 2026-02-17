from django.db import models

# Create your models here.


class Cart(models.Model):
    """Cart model representing a user's shopping cart."""
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='carts', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    """CartItem model representing an item in a user's shopping cart."""
    cart_item_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        'products.Product', on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    """Order model representing a user's order."""
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='orders')
    cart = models.OneToOneField(
        'Cart',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='order'
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.CharField(max_length=255)
    contactno = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)


class OrderItem(models.Model):
    """OrderItem model representing an item in a user's order."""
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        'products.Product', on_delete=models.CASCADE, related_name='order_items')
    cartitem = models.OneToOneField(
        'CartItem',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='orderitem'
    )
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def subtotal(self):
        """Return per-item subtotal (quantity * price) for templates and logic.

        This is a computed read-only property, not stored in the database.
        """
        return self.quantity * self.price
