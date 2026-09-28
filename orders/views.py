from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Order


@login_required
def order_list(request):

    orders = (
        Order.objects
        .filter(buyer=request.user)
        .prefetch_related("items__product")
        .order_by("-created_at")
    )

    return render(
        request,
        "orders.html",
        {
            "orders": orders
        }
    )


@login_required
def order_success(request, order_id):

    order = Order.objects.get(
        id=order_id,
        buyer=request.user
    )

    return render(
        request,
        "order_success.html",
        {
            "order": order
        }
    )

@login_required
def seller_orders(request):
    orders = (
        Order.objects
        .filter(items__product__seller=request.user)
        .prefetch_related("items__product", "buyer")
        .distinct()
        .order_by("-created_at")
    )

    return render(
        request,
        "seller_orders.html",
        {"orders": orders}
    )

@login_required
def update_seller_order_status(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        items__product__seller=request.user
    )

    if request.method == "POST":
        new_status = request.POST.get("status")

        allowed_statuses = [
            "pending",
            "confirmed",
            "processing",
            "completed",
            "cancelled",
        ]

        if new_status in allowed_statuses:
            order.status = new_status
            order.save(update_fields=["status", "updated_at"])

        return redirect("seller_orders")

    return redirect("seller_orders")