"""
URL patterns for Home application
"""

from django.urls import path
from product.views import ProductListView, ProductDetailView


urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),

]
