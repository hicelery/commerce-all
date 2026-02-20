"""Utility functions for discount code handling."""

from django.utils import timezone
from django.db import models
from products.models import DiscountCode


def validate_discount_code(code_string):
    """
    Validate a discount code string.

    Returns: (is_valid, discount_code_obj_or_none, error_message)
    """
    try:
        code = DiscountCode.objects.get(code__iexact=code_string.strip())
    except DiscountCode.DoesNotExist:
        return False, None, "Discount code not found."

    now = timezone.now()

    # Check if code is within valid date range
    if code.start_date > now:
        return False, None, "This discount code is not yet active."

    if code.end_date < now:
        return False, None, "This discount code has expired."

    # Check usage limit (if set)
    if code.max_uses and code.max_uses > 0:
        used_count = code.orders.filter(is_paid=True).count()
        if used_count >= code.max_uses:
            return False, None, "This discount code has reached its usage limit."

    return True, code, None


def apply_discount_to_items(cart_items, discount_code):
    """
    Calculate discounted prices for cart items based on discount code.

    Returns: dict with item discounts and total discount amount
    """
    if not discount_code:
        return {}

    discounts = {}
    total_discount = 0

    for item in cart_items:
        # Check if this item's category matches the code's category
        # or if the code applies to all categories (category is null)
        applies = (
            discount_code.category is None or
            item.product.category == discount_code.category
        )

        if applies:
            original_price = item.product.price
            discount_amount = original_price * \
                (discount_code.discount_percentage / 100)
            discounted_price = original_price - discount_amount
            total_discount += discount_amount * item.quantity

            discounts[item.cart_item_id] = {
                'original_price': original_price,
                'discount_percentage': discount_code.discount_percentage,
                'discount_amount': discount_amount,
                'discounted_price': discounted_price,
            }
        else:
            # Item doesn't qualify for discount, use normal price
            discounts[item.cart_item_id] = {
                'original_price': item.product.price,
                'discount_percentage': 0,
                'discount_amount': 0,
                'discounted_price': item.product.discounted_price,
            }

    return {
        'items': discounts,
        'total_discount': round(total_discount, 2),
        'code': discount_code,
    }
