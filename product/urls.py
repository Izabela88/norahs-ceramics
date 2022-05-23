"""
URL patterns for Home application
"""

from django.urls import path
from product.views import ProductsListView


urlpatterns = [
    path("", ProductsListView.as_view(), name="products_list"),
]
