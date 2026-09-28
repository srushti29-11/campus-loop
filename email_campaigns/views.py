from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.core.mail import send_mass_mail
from django.utils import timezone

from .models import EmailCampaign


User = get_user_model()


@staff_member_required
def create_campaign(request):

    if request.method == "POST":

        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()
        audience = request.POST.get("audience", "all")

        users = User.objects.filter(
            is_active=True
        ).exclude(email="")

        if audience == "active":
            users = users.filter(is_active=True)

        campaign = EmailCampaign.objects.create(
            created_by=request.user,
            subject=subject,
            message=message,
            audience=audience,
            status="draft",
            recipient_count=users.count()
        )

        messages = [
            (
                subject,
                message,
                None,
                [user.email]
            )
            for user in users
        ]

        send_mass_mail(
            messages,
            fail_silently=True
        )

        campaign.status = "sent"
        campaign.sent_at = timezone.now()
        campaign.save()

        return redirect("campaign_success")

    return render(
        request,
        "create_campaign.html"
    )


@staff_member_required
def campaign_success(request):

    return render(
        request,
        "campaign_success.html"
    )