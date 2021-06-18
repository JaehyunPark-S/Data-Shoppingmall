from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from products import models as product_models


class ProductInline(admin.TabularInline):
    model = product_models.Product


@admin.register(models.User)
class UserAdmin(UserAdmin):

    """ Custom User Admin """

    inlines = (ProductInline,)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "birthdate",
                    "superhost",
                )
            },
        ),
    )

    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "superhost",
        "is_staff",
        "is_superuser",
    )
