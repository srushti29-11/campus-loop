from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required


def home(request):
    return render(request, "home.html")


@staff_member_required
def admin_dashboard(request):
    from accounts.models import User
    from products.models import Product
    from orders.models import Order
    from payments.models import Payment
    from messages_app.models import Message
    from notifications.models import Notification
    from email_campaigns.models import EmailCampaign
    from revenue.models import Commission, Promotion
    from django.db.models import Sum

    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()

    successful_payments = Payment.objects.filter(
        status="success"
    ).count()

    total_messages = Message.objects.count()
    total_notifications = Notification.objects.count()
    total_campaigns = EmailCampaign.objects.count()

    commission_revenue = (
        Commission.objects.aggregate(
            total=Sum("commission_amount")
        )["total"] or 0
    )

    promotion_revenue = (
        Promotion.objects.filter(
            status="active"
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0
    )

    total_revenue = commission_revenue + promotion_revenue

    context = {
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
        "successful_payments": successful_payments,
        "total_messages": total_messages,
        "total_notifications": total_notifications,
        "total_campaigns": total_campaigns,
        "total_revenue": total_revenue,
    }

    return render(
        request,
        "admin_dashboard.html",
        context
    )

@staff_member_required
def admin_products(request):
    from products.models import Product

    products = (
        Product.objects
        .select_related("seller", "category")
        .order_by("-created_at")
    )

    status = request.GET.get("status", "").strip()

    if status:
        products = products.filter(status=status)

    search = request.GET.get("search", "").strip()

    if search:
        products = products.filter(
            name__icontains=search
        )

    return render(
        request,
        "admin_products.html",
        {
            "products": products,
            "selected_status": status,
            "search": search,
        }
    )

@staff_member_required
def admin_update_product_status(request, product_id):

    from products.models import Product
    from notifications.models import Notification

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == "POST":

        new_status = request.POST.get("status")

        if new_status in ["approved", "rejected"]:

            product.status = new_status
            product.save(update_fields=["status"])

            Notification.objects.create(
                user=product.seller,
                title=f"Product {new_status.title()}",
                message=(
                    f"Your product '{product.name}' "
                    f"has been {new_status} by the admin."
                ),
                notification_type="system"
            )

        return redirect("admin_products")

    return redirect("admin_products")

@staff_member_required
def admin_users(request):
    from accounts.models import User

    users = User.objects.all().order_by("-date_joined")

    search = request.GET.get("search", "").strip()

    if search:
        users = users.filter(
            email__icontains=search
        )

    return render(
        request,
        "admin_users.html",
        {
            "users": users,
            "search": search,
        }
    )

@staff_member_required
def admin_orders(request):
    from orders.models import Order

    orders = (
        Order.objects
        .select_related("buyer")
        .prefetch_related("items__product")
        .order_by("-created_at")
    )

    status = request.GET.get("status", "").strip()

    if status:
        orders = orders.filter(status=status)

    search = request.GET.get("search", "").strip()

    if search:
        orders = orders.filter(
            buyer__email__icontains=search
        )

    return render(
        request,
        "admin_orders.html",
        {
            "orders": orders,
            "selected_status": status,
            "search": search,
        }
    )

@staff_member_required
def admin_payments(request):
    from payments.models import Payment

    payments = (
        Payment.objects
        .select_related("buyer", "order")
        .order_by("-created_at")
    )

    status = request.GET.get("status", "").strip()

    if status:
        payments = payments.filter(status=status)

    search = request.GET.get("search", "").strip()

    from django.db.models import Q

    if search:
        payments = payments.filter(
            Q(buyer__first_name__icontains=search)
            | Q(buyer__last_name__icontains=search)
            | Q(buyer__email__icontains=search)
    )

    return render(
        request,
        "admin_payments.html",
        {
            "payments": payments,
            "selected_status": status,
            "search": search,
        }
    )

@staff_member_required
def admin_revenue(request):
    from django.db.models import Sum
    from revenue.models import Commission, Promotion

    commissions = (
        Commission.objects
        .select_related("seller", "order")
        .order_by("-created_at")
    )

    promotions = (
        Promotion.objects
        .select_related("seller", "product")
        .order_by("-created_at")
    )

    total_commission = (
        commissions.aggregate(
            total=Sum("commission_amount")
        )["total"] or 0
    )

    total_promotions = (
        promotions.filter(
            status="active"
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0
    )

    total_revenue = (
        total_commission + total_promotions
    )

    return render(
        request,
        "admin_revenue.html",
        {
            "commissions": commissions,
            "promotions": promotions,
            "total_commission": total_commission,
            "total_promotions": total_promotions,
            "total_revenue": total_revenue,
        }
    )

@staff_member_required
def admin_messages(request):
    from messages_app.models import Message

    messages_list = (
        Message.objects
        .select_related("sender", "receiver", "product")
        .order_by("-created_at")
    )

    search = request.GET.get("search", "").strip()

    if search:
        from django.db.models import Q

        messages_list = messages_list.filter(
            Q(sender__first_name__icontains=search)
            | Q(sender__last_name__icontains=search)
            | Q(sender__email__icontains=search)
            | Q(receiver__first_name__icontains=search)
            | Q(receiver__last_name__icontains=search)
            | Q(receiver__email__icontains=search)
            | Q(message__icontains=search)
        )

    return render(
        request,
        "admin_messages.html",
        {
            "messages_list": messages_list,
            "search": search,
        }
    )

@staff_member_required
def admin_notifications(request):
    from notifications.models import Notification
    from django.db.models import Q

    notifications_list = (
        Notification.objects
        .select_related("user")
        .order_by("-created_at")
    )

    search = request.GET.get("search", "").strip()
    notification_type = request.GET.get("type", "").strip()

    if search:
        notifications_list = notifications_list.filter(
            Q(user__first_name__icontains=search)
            | Q(user__last_name__icontains=search)
            | Q(user__email__icontains=search)
            | Q(title__icontains=search)
            | Q(message__icontains=search)
        )

    if notification_type:
        notifications_list = notifications_list.filter(
            notification_type=notification_type
        )

    return render(
        request,
        "admin_notifications.html",
        {
            "notifications_list": notifications_list,
            "search": search,
            "selected_type": notification_type,
        }
    )

