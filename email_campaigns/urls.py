from django.urls import path

from .views import create_campaign, campaign_success


urlpatterns = [
    path(
        "",
        create_campaign,
        name="create_campaign"
    ),
    path(
        "success/",
        campaign_success,
        name="campaign_success"
    ),
]