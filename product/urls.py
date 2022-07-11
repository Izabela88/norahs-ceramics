from django.urls import path
from product.views import ProductListView, ProductDetailView
from product.views import ReviewView


urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
    path(
        "<slug:slug>/review",
        ReviewView.as_view(),
        name="review",
    ),
]
