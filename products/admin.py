from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.ProductLanguage, models.ProductType)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = (
        "name",
        "used_by",
    )

    def used_by(self, obj):
        return obj.products.count()

    pass


class PhotoInline(admin.TabularInline):

    model = models.Photo


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):

    """ Product Admin Definition """

    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "name",
                    "description",
                    "price",
                    "upload_file",
                    "filename",
                )
            },
        ),
        ("Category", {"fields": ("product_type", "product_language")}),
        ("Last Details", {"fields": ("host",)}),
    )

    list_display = (
        "name",
        "price",
        "product_type",
        "product_language",
        "instant_book",
        "count_photos",
        "total_rating",
        "host",
    )

    list_filter = (
        "instant_book",
        "product_type",
        "product_language",
    )

    raw_id_fields = ("host",)

    search_fields = ("^name", "^host__username")

    def count_photos(self, obj):
        return obj.photos.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = (
        "__str__",
        "get_thumbnail",
    )

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"
