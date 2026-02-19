from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Order, OrderItem as OrderItems
from django.db import models
from .forms import ProfileUpdate


@login_required
def profile_view(request):
    queryset = Order.objects.filter(user=request.user).order_by(
        '-updated_at')
    items_count = {}
    # count number of order items, summed by quantity, for each order and store in a dict keyed by order_id
    for order in queryset:
        order_item_count = OrderItems.objects.filter(
            order=order).aggregate(
            total=models.Sum('quantity'))['total'] or 0
        items_count[order.order_id] = order_item_count
        # attach a transient attribute to the Order instance for template use
        setattr(order, 'items_count', order_item_count)

    return render(request, 'dashboard/account_centre.html', {
        'orders': queryset,
        'items_count': items_count,
    })


@login_required
def profile_page(request):
    # provide an unbound form for GET requests so fields render
    profile_form = ProfileUpdate(instance=request.user)
    return render(request,
                  'dashboard/profile.html',
                  {'profile_form': profile_form}
                  )


@login_required
def profile_update(request):
    # bind to POST when submitting and include the current user instance
    profile_form = ProfileUpdate(request.POST, instance=request.user)
    if request.method == 'POST':
        if profile_form.is_valid():
            profile_form.save()
            messages.info(request, 'Profile updated successfully.')
        else:
            messages.warning(request, 'Please correct the errors below.')
    return render(request, 'dashboard/profile.html', {'profile_form': profile_form})
