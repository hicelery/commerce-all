from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse


from .models import Cart, CartItem, Order, OrderItem
from products.models import Product, ProductSize
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
            cart, _ = Cart.objects.get_or_create(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.create(is_active=True)
        request.session['cart_id'] = cart.pk

    items = CartItem.objects.filter(cart=cart).select_related(
        'product')

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


def add_to_cart(request, product_id):
    # Use session-stored cart_id (or create/get a cart for the user)
    cart_id = request.session.get('cart_id')
    # Ensure we have a Cart instance
    if cart_id:
        try:
            cart = Cart.objects.get(pk=cart_id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user, is_active=True)
            request.session['cart_id'] = cart.cart_id
    else:
        if request.user.is_authenticated:
            try:
                # Prefer an active cart for the user; this avoids MultipleObjectsReturned
                cart, _ = Cart.objects.get_or_create(
                    user=request.user, is_active=True)
            except Cart.MultipleObjectsReturned:
                # If multiple carts exist, pick the most-recent one (highest pk) and use it.
                # This is defensive: it avoids crashing and provides a single cart to continue with.
                cart = Cart.objects.filter(
                    user=request.user, is_active=True).order_by('-pk').first()
                if not cart:
                    # As a last resort, pick any cart for the user or create a fresh one
                    cart = Cart.objects.filter(user=request.user).order_by(
                        '-pk').first() or Cart.objects.create(user=request.user, is_active=True)
        else:
            cart = Cart.objects.create()
        request.session['cart_id'] = cart.pk

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        print(f"Received POST data: {request.POST}")
        quantity = int(request.POST.get('quantity', 1))
        size = request.POST.get('size')
        cartitem, created = CartItem.objects.get_or_create(
            cart=cart, product=product, size=size)
        if not created:
            cartitem.quantity += quantity
        else:
            cartitem.quantity = quantity
        cartitem.save()
        messages.success(request, 'Item added to cart.')
    return redirect('cart:view_cart')


def update_cart_item(request, cart_id, cartitem_id):
    cart = get_object_or_404(Cart, pk=cart_id)
    cartitem = get_object_or_404(CartItem, pk=cartitem_id, cart=cart)

    # replace logic with update based on action (increase/decrease) or explicit quantity if provided
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            cartitem.quantity = max(
                cartitem.quantity + 1, cartitem.product.quantity)
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


def go_to_checkout(request):
    # ensure session key exists
    if not request.session.session_key:
        request.session.save()
        session_id = request.session.session_key
    else:
        session_id = request.session.session_key
    cart_id = request.session.get('cart_id')
    if cart_id:
        try:
            cart = Cart.objects.get(pk=cart_id)
        except Cart.DoesNotExist:
            cart = None
    # bounce user - maybe create guest user if not authenticated, but for now just require login to checkout
    if not request.user.is_authenticated:
        messages.info(
            request, 'You must be logged in to checkout. Log in here: <a href="/accounts/login">Login</a> or sign up here: <a href="/accounts/signup">Sign Up</a>.', extra_tags='safe')
        return redirect('cart:view_cart')

    # create order object first to get order_id for order items, then update total price after creating order items.
    try:
        order = Order.objects.get(cart=cart, user=request.user, is_paid=False)
    except Order.DoesNotExist:
        order = Order.objects.create(
            user=request.user, total_price=0, cart=cart)

    # Clear existing order items for this order to avoid duplicates
    # if user goes back to checkout after order creation but before
    # clearing cart
    OrderItem.objects.filter(order=order).delete()
    for item in CartItem.objects.filter(cart=cart):
        # add new order item for each cart item, linking back to cart item for reference but allowing order items to persist after cart is cleared
        try:
            OrderItem.objects.create(
                product=item.product,
                order=order,
                quantity=item.quantity,
                price=item.product.price,
                cartitem=item,
                size=item.size
            )
        # skip adding if item already exists (e.g. user goes back to checkout after order creation but before clearing cart)
        except Exception:
            pass
    # calculate subtotal and shipping for order summary, but total price will be updated at checkouts
    subtotal = sum(
        item.quantity * item.product.price for item in OrderItem.objects.filter(order=order)
    )
    shipping = 0 if subtotal >= 50 else 9.99
    order.total_price = subtotal + shipping
    order.is_paid = False
    order.save()
    context = {
        'session_id': session_id,
        'cart_id': cart.pk if cart else None,
        'order': order,
        'subtotal': subtotal,
        'shipping': shipping,
    }
    return render(request, 'cart/checkout.html', context)


def checkout(request, order_id=None):
    # Resolve order: prefer explicit arg, then POST/GET, then user's unpaid order
    if order_id is None:
        order_id = request.POST.get('order_id') or request.GET.get('order_id')
    order = None
    if order_id:
        order = get_object_or_404(Order, pk=order_id)
    else:
        if request.user.is_authenticated:
            order = Order.objects.filter(
                user=request.user, is_paid=False).last()
        if not order:
            # no order found to process
            return redirect('cart:view_cart')

    # with order, update shipping address and mark as paid, then clear cart items and create new cart for session
    if request.method == 'POST':
        # build shipping_address from submitted fields so form validation succeeds
        post_data = request.POST.copy()
        first_name = post_data.get('first_name', '').strip()
        last_name = post_data.get('last_name', '').strip()
        address = post_data.get('address', '').strip()
        city = post_data.get('city', '').strip()
        phone = post_data.get('phone', '').strip()
        state = post_data.get('state', '').strip()
        zipcode = post_data.get('zipcode', '').strip()
        shipping_address = ', '.join(filter(
            None, [f"{first_name} {last_name}".strip(), address, city, state, zipcode]))
        post_data['shipping_address'] = shipping_address

        checkout_form = CheckoutForm(data=post_data, user=request.user)
        print(f"Checkout form data: {post_data}")
        if checkout_form.is_valid():
            # prefer cleaned value but fallback to our assembled address
            shipping_address = checkout_form.cleaned_data.get(
                'shipping_address') or shipping_address
            order.is_paid = True  # Mark order as paid
            order.shipping_address = shipping_address
            order.contactno = phone  # Save phone number to order
            order.save()
            cart = order.cart
            cart_id = cart.pk if cart else None
            # Clear cart items for the paid cart
            if cart:
                CartItem.objects.filter(cart=cart).delete()
            elif cart_id:
                CartItem.objects.filter(cart_id=cart_id).delete()

            # close out old cart and create new one for session
            cart.is_active = False
            cart.save()

            # Create a fresh cart for the user and store it in session
            if request.user.is_authenticated:
                new_cart = Cart.objects.create(
                    user=request.user, is_active=True)
            else:
                new_cart = Cart.objects.create(is_active=True)
            request.session['cart_id'] = new_cart.pk
        else:
            messages.error(
                request, f'Please fix form errors: {checkout_form.errors}')
            return render(request, 'cart/checkout.html', {'order': order, 'form': checkout_form})
        context = {'order': order,
                   'shipping_address': order.shipping_address, 'phone': phone}
        print(context)

    return redirect('cart:order_confirmation', order_id=order.pk)


def order_confirmation(request, order_id):
    # get order
    # get associated items
    order = get_object_or_404(Order, pk=order_id)
    # collect order items; per-item subtotal is available via model property
    order_items = order.items.select_related('product').all()
    subtotal = sum(order_item.subtotal for order_item in order_items)
    context = {'order': order,
               'order_items': order_items, 'subtotal': subtotal}
    return render(request, 'cart/order_confirmation.html', context)
