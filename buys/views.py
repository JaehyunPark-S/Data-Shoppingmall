from django.shortcuts import redirect, reverse
from django.contrib import messages
from products import models as product_models
from . import models


def create(request, product):
    try:
        product = product_models.Product.objects.get(pk=product)
        buy = models.Buy.objects.create(
            buyer=request.user,
            product=product,
            status=models.Buy.STATUS_BOUGHT,
        )
        return redirect(reverse("products:detail", kwargs={"pk": buy.product.pk}))
    except product_models.Product.DoesNotExist:
        messages.error(request, "Can't Buy That Product")
        return redirect(reverse("core:home"))
