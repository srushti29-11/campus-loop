from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render

from .models import Message
from notifications.models import Notification

User = get_user_model()


@login_required
def messages_view(request):
    received = Message.objects.filter(
        receiver=request.user
    ).select_related(
        "sender", "product"
    ).order_by("-created_at")

    sent = Message.objects.filter(
        sender=request.user
    ).select_related(
        "receiver", "product"
    ).order_by("-created_at")

    return render(
        request,
        "messages.html",
        {
            "received": received,
            "sent": sent
        }
    )


@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(
        User,
        id=receiver_id
    )

    product_id = request.GET.get("product")
    product = None

    if product_id:
        from products.models import Product

        product = get_object_or_404(
            Product,
            id=product_id
        )

    if request.method == "POST":
        message_text = request.POST.get(
            "message",
            ""
        ).strip()

        if message_text:
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                product=product,
                message=message_text
            )

            Notification.objects.create(
                user=receiver,
                title="New Message",
                message=(
                    f"You received a new message from "
                    f"{request.user.first_name or request.user.email}."
                ),
                notification_type="message"
            )

        return redirect("messages")

    return render(
        request,
        "send_message.html",
        {
            "receiver": receiver,
            "product": product
        }
    )