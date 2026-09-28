from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # Admin
    path("admin/", admin.site.urls),

    # Home + Authentication + Dashboard
    path("", include("core.urls")),
    path("", include("accounts.urls")),

    # Products
    path("products/", include("products.urls")),

    # Cart
    path("cart/", include("cart.urls")),

    # Orders
    path("orders/", include("orders.urls")),

    # Messages
    path("messages/", include("messages_app.urls")),

    # Notifications
    path("notifications/", include("notifications.urls")),

    # Payments
    path("payments/", include("payments.urls")),

    # Revenue
    path("revenue/", include("revenue.urls")),

    # Email Campaigns
    path(
        "email-campaigns/",
        include("email_campaigns.urls")
    ),
]


# Product Images / Media Files
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)