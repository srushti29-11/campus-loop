from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from orders.models import Order
from notifications.models import Notification
from revenue.models import Commission
from .models import Payment


@login_required
def payment_page(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        buyer=request.user
    )

    # If already paid, don't create another payment
    existing_payment = Payment.objects.filter(
        order=order,
        status="success"
    ).first()

    if existing_payment:
        return redirect(
            "payment_success",
            order_id=order.id
        )

    if request.method == "POST":

        payment_method = request.POST.get(
            "payment_method",
            "test_card"
        )

        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={
                "buyer": request.user,
                "amount": order.total_amount,
                "payment_method": payment_method,
                "status": "success",
                "transaction_id": f"TEST-{order.id}",
            }
        )

        if not created and payment.status != "success":
            payment.payment_method = payment_method
            payment.status = "success"
            payment.transaction_id = f"TEST-{order.id}"
            payment.save()

        # Confirm order
        order.status = "confirmed"
        order.save(update_fields=["status", "updated_at"])

        # Create commission only once
        if not Commission.objects.filter(order=order).exists():
            order.create_commissions()

        # Create buyer notification only once
        if not Notification.objects.filter(
            user=request.user,
            title="Payment Successful",
            message__contains=f"Order #{order.id}"
        ).exists():

            Notification.objects.create(
                user=request.user,
                title="Payment Successful",
                message=(
                    f"Payment for Order #{order.id} was successful. "
                    f"Your order has been confirmed."
                ),
                notification_type="payment"
            )

        return redirect(
            "payment_success",
            order_id=order.id
        )

    return render(
        request,
        "payment.html",
        {
            "order": order
        }
    )


@login_required
def payment_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        buyer=request.user
    )

    payment = get_object_or_404(
        Payment,
        order=order
    )

    return render(
        request,
        "payment_success.html",
        {
            "order": order,
            "payment": payment
        }
    )