from django.contrib import admin
from . import models


@admin.register(models.Buy)
class BuyAdmin(admin.ModelAdmin):

    """ Buy Admin Definition """

    list_display = ("product", "status", "buyer")
