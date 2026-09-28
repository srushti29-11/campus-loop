from django.urls import path

from .views import messages_view, send_message


urlpatterns = [
    path("", messages_view, name="messages"),
    path(
        "send/<int:receiver_id>/",
        send_message,
        name="send_message"
    ),
]