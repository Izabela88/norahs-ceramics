"""
URL patterns for Home application
"""

from django.urls import path
from product.views import Products


urlpatterns = [
    path("", Products.as_view(), name="products"),
]