from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("create/<int:product>/", views.create_review, name="create"),
    path("delete/<int:pk>/", views.delete_review, name="delete"),
    path(
        "<int:product_pk>/edit/<int:review_pk>/",
        views.ReviewUpdateView.as_view(),
        name="edit",
    ),
]
