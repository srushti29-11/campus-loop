from django.urls import path

from .views import revenue_dashboard


urlpatterns = [
    path(
        "",
        revenue_dashboard,
        name="revenue_dashboard"
    ),
]