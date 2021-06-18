from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from products import models as product_models
from users import mixins as user_mixins
from django.http import Http404
from . import forms, models


def create_review(request, product):
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        product = product_models.Product.objects.get_or_none(pk=product)
        if not product:
            return redirect(reverse("core:home"))
        if form.is_valid():
            review = form.save()
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Product reviewed")
            return redirect(reverse("products:detail", kwargs={"pk": product.pk}))
        if not form.is_valid():
            return redirect(reverse("core:home"))


@login_required
def delete_review(request, pk):
    user = request.user
    try:
        review = models.Review.objects.get(pk=pk)
        if review.user.pk != user.pk:
            messages.error(request, "Can't delete that Review")
        else:
            review.delete()
            messages.success(request, "Review Deleted")
            return redirect(
                reverse("products:detail", kwargs={"pk": review.product.pk})
            )
    except models.Review.DoesNotExist:
        return redirect(reverse("core:home"))


class ReviewUpdateView(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.Review
    template_name = "reviews/review_edit.html"
    pk_url_kwarg = "review_pk"
    fields = (
        "review",
        "thumbs_up",
    )

    def get_success_url(self):
        product_pk = self.kwargs.get("product_pk")
        messages.success(self.request, "Review Updated")
        return reverse("products:detail", kwargs={"pk": product_pk})
