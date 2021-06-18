from django.urls import path
from . import views

app_name = "buys"

urlpatterns = [
    path(
        "create/<int:product>/",
        views.create,
        name="create",
    ),
]
