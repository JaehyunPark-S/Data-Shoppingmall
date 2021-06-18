from django.db import models
from core import models as core_models
from django.shortcuts import reverse
from django.http import HttpResponse
from uuid import uuid4
from datetime import datetime


def get_file_path(instance, filename):
    ymd_path = datetime.now().strftime("%Y/%m/%d")
    uuid_name = uuid4().hex
    return "/".join(["product_datas/", ymd_path, uuid_name])


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class ProductLanguage(AbstractItem):

    """ Product Language Definition """

    pass

    class Meta:
        verbose_name_plural = "Product Languages"
        ordering = ["name"]


class ProductType(AbstractItem):

    """ Product Object Definition """

    pass

    class Meta:
        verbose_name_plural = "Product Types"
        ordering = ["name"]


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="product_photos")
    product = models.ForeignKey(
        "Product", related_name="photos", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.caption


class Product(core_models.TimeStampedModel):

    """ Product Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()
    price = models.IntegerField()
    upload_file = models.FileField(upload_to=get_file_path, null=True, blank=True)
    filename = models.CharField(max_length=64, null=True)
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User", related_name="products", on_delete=models.CASCADE
    )
    product_type = models.ForeignKey(
        "ProductType", on_delete=models.SET_NULL, related_name="products", null=True
    )
    product_language = models.ForeignKey(
        "ProductLanguage", on_delete=models.SET_NULL, related_name="products", null=True
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if not len(all_reviews):
            return 0
        for review in all_reviews:
            all_ratings += review.rating()
        return round(all_ratings / len(all_reviews), 2)

    def first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        return photos
