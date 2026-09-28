from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import User


def login_view(request):

    if request.method == "POST":

        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.is_staff:
                return redirect("admin_dashboard")

            return redirect("home")

        return render(
            request,
            "login.html",
            {
                "error": "Invalid email or password."
            }
        )

    return render(request, "login.html")


def register_view(request):

    if request.method == "POST":

        # Get form data
        email = request.POST.get(
            "email",
            ""
        ).strip().lower()

        password = request.POST.get(
            "password",
            ""
        )

        first_name = request.POST.get(
            "first_name",
            ""
        ).strip()

        last_name = request.POST.get(
            "last_name",
            ""
        ).strip()

        college = request.POST.get(
            "college",
            ""
        ).strip()


        # Basic validation
        if not email or not password:

            return render(
                request,
                "register.html",
                {
                    "error": "Email and password are required."
                }
            )


        # Check whether email already exists
        if User.objects.filter(
            email__iexact=email
        ).exists():

            return render(
                request,
                "register.html",
                {
                    "error": (
                        "An account with this email "
                        "already exists. Please login."
                    )
                }
            )


        # Create user
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            college=college
        )


        # Login immediately after registration
        login(
            request,
            user
        )

        messages.success(
            request,
            "Your account has been created successfully."
        )

        return redirect("home")


    return render(
        request,
        "register.html"
    )


def logout_view(request):

    logout(request)

    return redirect("home")


@login_required
def dashboard(request):

    from products.models import Product
    from orders.models import Order
    from cart.models import CartItem
    from notifications.models import Notification


    # Products listed by this user
    my_products = (
        Product.objects
        .filter(
            seller=request.user
        )
        .order_by("-created_at")
    )


    # Orders purchased by this user
    order_count = (
        Order.objects
        .filter(
            buyer=request.user
        )
        .count()
    )


    # Cart items
    cart_count = (
        CartItem.objects
        .filter(
            buyer=request.user
        )
        .count()
    )


    # Unread notifications
    unread_notifications = (
        Notification.objects
        .filter(
            user=request.user,
            is_read=False
        )
        .count()
    )


    context = {

        "my_products": my_products,

        "order_count": order_count,

        "cart_count": cart_count,

        "unread_notifications":
            unread_notifications,

    }


    return render(
        request,
        "dashboard.html",
        context
    )