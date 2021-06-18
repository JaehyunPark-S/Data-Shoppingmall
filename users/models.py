from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from django.db import models


class User(AbstractUser):

    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    avatar = models.ImageField(upload_to="avatars", blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    birthdate = models.DateField(blank=True, null=True)
    superhost = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})

    def get_buyers(self):
        return self.buys.all
