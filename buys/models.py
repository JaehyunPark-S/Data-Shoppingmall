from django.db import models
from core import models as core_models


class Buy(core_models.TimeStampedModel):

    """ Reservationn Model Definition """

    STATUS_BOUGHT = "bought"
    STATUS_NOTBUY = "notbuy"

    STATUS_CHOICES = (
        (STATUS_BOUGHT, "Bought"),
        (STATUS_NOTBUY, "Not Buy"),
    )
    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_NOTBUY
    )
    buyer = models.ForeignKey(
        "users.User", related_name="buys", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        "products.Product", related_name="buys", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.product}"
