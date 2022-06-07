from django.urls import path
from basket.views import Basket


urlpatterns = [
    path("", Basket.as_view(), name="basket"),
]