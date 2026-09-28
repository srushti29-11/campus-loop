from django.urls import path

from .views import (
    home, 
    admin_dashboard, 
    admin_products, 
    admin_update_product_status,
    admin_users,
    admin_orders,
    admin_payments,
    admin_revenue,
    admin_messages,
    admin_notifications,
)



urlpatterns = [

    path("", home, name="home"),

    path(
        "admin-dashboard/",
        admin_dashboard,
        name="admin_dashboard"
    ),

    path(
    "admin-dashboard/products/",
    admin_products,
    name="admin_products"
),

    path(
        "admin-dashboard/products/update/<int:product_id>/",
        admin_update_product_status,
        name="admin_update_product_status"
),

path(
    "admin-dashboard/users/",
    admin_users,
    name="admin_users"
),

path(
    "admin-dashboard/orders/",
    admin_orders,
    name="admin_orders"
),

path(
    "admin-dashboard/payments/",
    admin_payments,
    name="admin_payments"
),

path(
    "admin-dashboard/revenue/",
    admin_revenue,
    name="admin_revenue"
),

path(
    "admin-dashboard/messages/",
    admin_messages,
    name="admin_messages"
),

path(
    "admin-dashboard/notifications/",
    admin_notifications,
    name="admin_notifications"
),
]