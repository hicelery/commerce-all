from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cart.models import Order, OrderItem as OrderItems


@login_required
def profile_view(request):
    queryset = Order.objects.filter(user=request.user).order_by(
        '-updated_at')
    items_count = {}
    # count number of order items in each order and attach to each Order
    for order in queryset:
        order_item_count = OrderItems.objects.filter(order=order).count()
        items_count[order.order_id] = order_item_count
        # attach a transient attribute to the Order instance for template use
        setattr(order, 'items_count', order_item_count)

    return render(request, 'dashboard/account_centre.html', {
        'orders': queryset,
        'items_count': items_count,
    })
