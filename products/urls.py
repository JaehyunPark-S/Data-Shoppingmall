from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("create/", views.CreateProductView.as_view(), name="create"),
    path("<int:pk>", views.ProductDetail.as_view(), name="detail"),
    path("<int:pk>/delete/", views.delete_product, name="delete-product"),
    path("<int:pk>/edit/", views.EditProductView.as_view(), name="edit"),
    path("<int:pk>/photos/", views.ProductPhotosView.as_view(), name="photos"),
    path("<int:pk>/photos/add/", views.AddPhotoView.as_view(), name="add-photo"),
    path(
        "<int:product_pk>/photos/<int:photo_pk>/delete",
        views.delete_photo,
        name="delete-photo",
    ),
    path(
        "<int:product_pk>/photos/<int:photo_pk>/edit",
        views.EditPhotoView.as_view(),
        name="edit-photo",
    ),
    path("search/", views.SearchView.as_view(), name="search"),
    path("download/<int:pk>", views.product_download_view, name="product_download"),
]
