from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from shop.forms import ProductFiltersForm, PurchasesFiltersForm
from shop.models import Product, Purchase
from shop.services import filter_products


class ProductsView(TemplateView):
    template_name = "products/list.html"

    def get_context_data(self, **kwargs):
        products = Product.objects.all()
        filters_form = ProductFiltersForm(self.request.GET)

        if filters_form.is_valid():
            products = filter_products(products, **filters_form.cleaned_data)

        paginator = Paginator(products, 3)
        page_number = self.request.GET.get("page")
        products = paginator.get_page(page_number)

        return {"filters_form": filters_form, "products": products}


def product_details_view(request, *args, **kwargs):
    product = Product.objects.get(id=kwargs["product_id"])

    # Add to favorites if this is POST request
    if request.user.is_authenticated and request.method == "POST":
        if request.POST["action"] == "add":
            product.favorites.add(request.user)
            messages.info(request, "Product successfully added to favorites")
        elif request.POST["action"] == "remove":
            product.favorites.remove(request.user)
            messages.info(request, "Product successfully removed to favorites")
        elif request.POST["action"] == "purchase":
            Purchase.objects.create(product=product, user=request.user, count=int(request.POST["count"]))
            messages.info(request, "Product successfully purchased!")
        redirect("product_details_view", product_id=product.id)

    return render(
        request,
        "products/details.html",
        {
            "product": product,
            "is_product_in_favorites": request.user in product.favorites.all(),
        },
    )


class PurchaseView(TemplateView):
    template_name = "products/purchases.html"

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            raise Http404
        purchases = Purchase.objects.filter(user=self.request.user)
        filters_form = PurchasesFiltersForm(self.request.GET)
        if filters_form.is_valid() and filters_form.cleaned_data["order_by"]:
            purchases = purchases.order_by(filters_form.cleaned_data["order_by"])
        return {"purchases": purchases, "filters_form": filters_form}