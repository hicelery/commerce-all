from urllib import request
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from cart.models import Cart, CartItem

# Create your views here.


def cart_detail(request):
    cart_id = request.session.get('cart_id')
    cart, created = Cart.objects.get_or_create(
        cart_id=cart_id, user=request.user)
    cartitems = CartItem.objects.filter(cart=cart)
    context = {'cart': cart, 'cartitems': cartitems}
    return render(request, 'cart/view_cart.html', context)


def update_cart_item(request, cart_id, product_id):
    cart = Cart.objects.get(id=cart_id)
    cartitems = CartItem.objects.filter(cart=cart, user=request.user)
    cartitem = cartitems.get(product_id=product_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
    cartitem.quantity = quantity
    cartitem.save()
    context = {'cart': cart, 'cartitems': cartitems}
    return render(request,
                  'cart/cart_detail.html',
                  context)


def remove_from_cart(request, cartitem_id,):
    cartitem = CartItem.objects.get(id=cartitem_id)
    cartitem.delete()
    messages.add_message(request, messages.SUCCESS, 'Item removed!')

    return HttpResponseRedirect('cart:view_cart', args=[cartitem.cart.id])


def add_to_cart(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity', 1))
        cartitem, created = CartItem.objects.get_or_create(
            cart=cart, product_id=product_id)
        if not created:
            cartitem.quantity += quantity
        else:
            cartitem.quantity = quantity
        cartitem.save()

    context = {'cart': cart}
    return render(request,
                  'cart/cart_detail.html',
                  context)
