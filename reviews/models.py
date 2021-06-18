from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core import models as core_models


class Review(core_models.TimeStampedModel):

    """ Review Model Definition """

    review = models.TextField()
    thumbs_up = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        "products.Product", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.review} - {self.product}"

    def rating(self):
        return round(self.thumbs_up, 2)

    class Meta:
        ordering = ("-created",)
