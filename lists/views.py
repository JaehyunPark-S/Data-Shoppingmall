from django.shortcuts import reverse, redirect
from django.views.generic import TemplateView
from products import models as product_models
from . import models


def toggle_product(request, product_pk):
    action = request.GET.get("action", None)
    product = product_models.Product.objects.get_or_none(pk=product_pk)
    if product is not None and action is not None:
        the_list, created = models.List.objects.get_or_create(
            user=request.user, name="My Favourites Program"
        )
        if action == "add":
            the_list.products.add(product)
        elif action == "remove":
            the_list.products.remove(product)
        return redirect(reverse("products:detail", kwargs={"pk": product_pk}))


class SeeFavsView(TemplateView):

    template_name = "lists/list_detail.html"
