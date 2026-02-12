from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse


from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from .forms import CheckoutForm

# Create your views here.


def cart_detail(request, cart_id=None):
    # Resolve cart from session or create one. Support anonymous carts.
    cart_id = request.session.get('cart_id')
    cart = None
    if cart_id:
        try:
            cart = Cart.objects.get(pk=cart_id)
        except Cart.DoesNotExist:
            cart = None

    if not cart:
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            cart = Cart.objects.create()
        request.session['cart_id'] = cart.pk

    items = CartItem.objects.filter(cart=cart).select_related('product')

    subtotal = sum(item.quantity * item.product.price for item in items)
    if subtotal >= 50:
        shipping = 0
    else:
        shipping = 9.99

    context = {
        'cart': cart,
        'items': items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': subtotal + shipping,
        'items_count': items.count(),
        'session_cart_id': request.session.get('cart_id'),

    }
    return render(request, 'cart/view_cart.html', context)


def update_cart_item(request, cart_id, cartitem_id):
    cart = get_object_or_404(Cart, pk=cart_id)
    cartitem = get_object_or_404(CartItem, pk=cartitem_id, cart=cart)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            cartitem.quantity = cartitem.quantity + 1
        elif action == 'decrease':
            cartitem.quantity = max(1, cartitem.quantity - 1)
        else:
            # fallback to explicit quantity if provided
            try:
                quantity = int(request.POST.get('quantity', cartitem.quantity))
            except (TypeError, ValueError):
                quantity = cartitem.quantity
            cartitem.quantity = max(1, quantity)
        cartitem.save()
        messages.success(request, 'Cart updated.')
    return redirect('cart:view_cart')


def remove_from_cart(request, cart_id, cartitem_id):
    cart = get_object_or_404(Cart, pk=cart_id)
    cartitem = get_object_or_404(CartItem, pk=cartitem_id, cart=cart)
    cartitem.delete()
    messages.success(request, 'Item removed!')
    return redirect('cart:view_cart')


def add_to_cart(request, product_id):
    # Use session-stored cart_id (or create/get a cart for the user)
    cart_id = request.session.get('cart_id')
    # Ensure we have a Cart instance
    if cart_id:
        try:
            cart = Cart.objects.get(pk=cart_id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)
            request.session['cart_id'] = cart.cart_id
    else:
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            cart = Cart.objects.create()
        request.session['cart_id'] = cart.pk

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cartitem, created = CartItem.objects.get_or_create(
            cart=cart, product=product)
        if not created:
            cartitem.quantity += quantity
        else:
            cartitem.quantity = quantity
        cartitem.save()
        messages.success(request, 'Item added to cart.')
        return redirect('cart:view_cart')

    # If GET, show cart
    return redirect('cart:view_cart')


def clear_cart(request):
    if request.method == 'POST':
        cart_id = request.session.get('cart_id')
        if cart_id:
            CartItem.objects.filter(cart_id=cart_id).delete()
        messages.success(request, 'Cart cleared.')
    return redirect('cart:view_cart')


def apply_discount(request):
    # Placeholder: accept promo code but do not apply logic yet
    if request.method == 'POST':
        promo = request.POST.get('promo_code')
        messages.info(request, f'Promo code "{promo}" is not implemented.')
    return redirect('cart:view_cart')


def checkout(request):
    # Minimal placeholder for checkout route
    # In a real implementation, this would handle payment processing, order creation, etc.
    # For now, give order confirmation and clear cart as a placeholder
    # move items from cart into order/order items.
    if request.method == 'POST':
        checkout_form = CheckoutForm(data=request.POST, user=request.user)
        cart_id = request.session.get('cart_id')
        total_price = sum(
            item.quantity * item.product.price for item in CartItem.objects.filter(cart_id=cart_id))
        order = Order.objects.create(
            user=request.user, total_price=total_price)
    # Insert each CartItem into OrderItem
        for item in CartItem.objects.filter(cart_id=cart_id):
            OrderItem.objects.create(product=item.product, order_id=order.order_id,
                                     quantity=item.quantity, price=item.product.price)
        CartItem.objects.filter(cart_id=cart_id).delete()  # Clear cart
    return render(request, 'cart/checkout.html')
