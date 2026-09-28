from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product
from orders.models import Order, OrderItem
from notifications.models import Notification
from .models import CartItem


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        status="approved"
    )

    # User cannot add their own product
    if product.seller == request.user:
        return redirect("product_detail", product_id=product.id)

    cart_item, created = CartItem.objects.get_or_create(
        buyer=request.user,
        product=product
    )

    if not created:

        if cart_item.quantity >= product.stock:
            return redirect(
                "product_detail",
                product_id=product.id
        )

    cart_item.quantity += 1
    cart_item.save()

    return redirect("cart")


@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(
        buyer=request.user
    ).select_related("product")

    total = sum(
        item.total_price
        for item in cart_items
    )

    return render(
        request,
        "cart.html",
        {
            "cart_items": cart_items,
            "total": total
        }
    )


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        buyer=request.user
    )

    item.delete()

    return redirect("cart")


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(
        buyer=request.user
    ).select_related("product")

    if not cart_items.exists():
        return redirect("cart")

    total = sum(
        item.total_price
        for item in cart_items
    )

    if request.method == "POST":
        for item in cart_items:
            if item.quantity > item.product.stock:
                return redirect("cart")

        address = request.POST.get(
            "delivery_address",
            ""
        ).strip()

        order = Order.objects.create(
            buyer=request.user,
            total_amount=total,
            delivery_address=address,
            status="pending"
        )

    for item in cart_items:

        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
         )

        item.product.stock -= item.quantity

        if item.product.stock == 0:
            item.product.status = "sold"

        item.product.save(
            update_fields=["stock", "status"]
        )

        Notification.objects.create(
            user=item.product.seller,
            title="New Order Received",
            message=(
                f"Your product '{item.product.name}' "
                f"has been ordered. Order #{order.id}."
            ),
            notification_type="order"
        )

        cart_items.delete()

        return redirect(
            "payment_page",
             order_id=order.id
        )

    return render(
        request,
        "checkout.html",
        {
            "cart_items": cart_items,
            "total": total
        }
    )