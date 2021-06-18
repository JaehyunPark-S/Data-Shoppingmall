from django.urls import path
from . import views

app_name = "lists"

urlpatterns = [
    path("toggle/<int:product_pk>", views.toggle_product, name="toggle-product"),
    path("favs/", views.SeeFavsView.as_view(), name="see-favs"),
]
