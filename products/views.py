from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Category, Product


def product_list(request):

    products = Product.objects.filter(
        status="approved"
    ).select_related("category", "seller")

    search = request.GET.get("search", "").strip()
    category_id = request.GET.get("category", "")
    listing_type = request.GET.get("listing_type", "").strip()

    if search:
        products = products.filter(
            name__icontains=search
        )

    if category_id:
        products = products.filter(
            category_id=category_id
        )

    if listing_type:
        products = products.filter(listing_type=listing_type)

    categories = Category.objects.all().order_by("name")

    return render(
        request,
        "products.html",
        {
            "products": products,
            "categories": categories,
            "search": search,
            "selected_category": category_id,
            "selected_listing_type": listing_type,
        }
    )


def product_detail(request, product_id):

    product = get_object_or_404(
        Product.objects.select_related(
            "category",
            "seller"
        ),
        id=product_id,
        status="approved"
    )

    return render(
        request,
        "product_detail.html",
        {
            "product": product
        }
    )


@login_required
def add_product(request):

    categories = Category.objects.all().order_by("name")

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        category_id = request.POST.get("category")
        description = request.POST.get("description", "").strip()
        price = request.POST.get("price", "0")
        condition = request.POST.get("condition", "good")
        stock = request.POST.get("stock", "1")
        listing_type = request.POST.get("listing_type", "buy")
        if listing_type == "free":
            price = 0

        image = request.FILES.get("image")

        category = get_object_or_404(
            Category,
            id=category_id
        )

        Product.objects.create(
            name=name,
            seller=request.user,
            category=category,
            description=description,
            price=price,
            condition=condition,
            stock=stock,
            listing_type=listing_type,
            image=image,
            status="pending"
        )

        return redirect("dashboard")

    return render(
        request,
        "add_product.html",
        {
            "categories": categories
        }
    )