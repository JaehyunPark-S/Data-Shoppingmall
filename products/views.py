from django.views.generic import (
    ListView,
    DetailView,
    View,
    UpdateView,
    CreateView,
    FormView,
)
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from users import mixins as user_mixins
from . import models, forms
from reviews import forms as review_forms
import urllib
import os
import mimetypes


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Product
    paginate_by = 12
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "products"


class ProductDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = review_forms.CreateReviewForm()
        return context


class SearchView(View):
    def get(self, request):
        name = request.GET.get("name")

        if name:

            form = forms.SearchForm(request.GET)
            if form.is_valid():
                name = form.cleaned_data.get("name")
                product_type = form.cleaned_data.get("product_type")
                product_language = form.cleaned_data.get("product_language")
                price = form.cleaned_data.get("price")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")

                filter_args = {}

                if name != "Anything":
                    filter_args["name__startswith"] = name

                if product_type is not None:
                    filter_args["product_type"] = product_type

                if product_language is not None:
                    filter_args["product_language"] = product_language

                if price is not None:
                    filter_args["price__lte"] = price

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                products = models.Product.objects.filter(**filter_args)

                products = products.order_by("-created")

                paginator = Paginator(products, 100)

                page = request.GET.get("page", 1)

                products = paginator.get_page(page)

                if product_type is None:
                    product_type = ""
                if product_language is None:
                    product_type = ""
                if price is None:
                    price = ""
                current_url = f"/products/search/?name={name}&product_type={product_type}&product_language={product_language}&price={price}"

                if instant_book is True:
                    current_url = current_url + "&instant_book=on"
                if superhost is True:
                    current_url = current_url + "&superhost=on"
                print(current_url)
                return render(
                    request,
                    "products/search.html",
                    {"form": form, "products": products, "path": current_url},
                )
        else:
            form = forms.SearchForm()

        return render(request, "products/search.html", {"form": form})


def product_download_view(request, pk):
    product = get_object_or_404(models.Product, pk=pk)
    url = product.upload_file.url[1:]
    file_url = urllib.parse.unquote(url)
    if os.path.exists(file_url):
        with open(file_url, "rb") as fh:
            quote_file_url = urllib.parse.quote(product.filename.encode("utf-8"))
            response = HttpResponse(
                fh.read(), content_type=mimetypes.guess_type(file_url)[0]
            )
            response["Content-Disposition"] = (
                "attachment; filename*=UTF-8''%s" % quote_file_url
            )
            return response
        raise Http404


@login_required
def delete_product(request, pk):
    user = request.user
    try:
        product = models.Product.objects.get(pk=pk)
        if product.host.pk != user.pk:
            messages.error(request, "Cant delete that photo")
        else:
            product.delete()
            messages.success(request, "Product Deleted")
            return redirect(reverse("core:home"))
    except models.Product.DoesNotExist:
        return redirect(reverse("core:home"))


class EditProductView(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.Product
    template_name = "products/product_edit.html"
    fields = (
        "name",
        "description",
        "price",
        "filename",
    )

    def get_object(self, queryset=None):
        product = super().get_object(queryset=queryset)
        if product.host.pk != self.request.user.pk:
            raise Http404()
        return product


class ProductPhotosView(user_mixins.LoggedInOnlyView, DetailView):
    model = models.Product
    template_name = "products/product_photos.html"

    def get_object(self, queryset=None):
        product = super().get_object(queryset=queryset)
        if product.host.pk != self.request.user.pk:
            raise Http404()
        return product


@login_required
def delete_photo(request, product_pk, photo_pk):
    user = request.user
    try:
        product = models.Product.objects.get(pk=product_pk)
        if product.host.pk != user.pk:
            messages.error(request, "Can't delete that photo")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo Deleted")
            return redirect(reverse("products:photos", kwargs={"pk": product_pk}))
    except models.Product.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = "products/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    success_message = "Photo Updated"
    fields = ("caption",)

    def get_success_url(self):
        product_pk = self.kwargs.get("product_pk")
        return reverse("products:photos", kwargs={"pk": product_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):

    template_name = "products/photo_create.html"
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo Uploaded")
        return redirect(reverse("products:photos", kwargs={"pk": pk}))


class CreateProductView(user_mixins.LoggedInOnlyView, FormView):
    form_class = forms.CreateProductForm
    template_name = "products/product_create.html"

    def form_valid(self, form):
        product = form.save()
        product.host = self.request.user
        product.save()
        messages.success(self.request, "Product Create")
        return redirect(reverse("products:detail", kwargs={"pk": product.pk}))
