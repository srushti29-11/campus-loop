from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect


@staff_member_required
def revenue_dashboard(request):
    return redirect("admin_revenue")