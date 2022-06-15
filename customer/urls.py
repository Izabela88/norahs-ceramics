from django.urls import path
from customer.views import CustomerProfileView


urlpatterns = [
    path("", CustomerProfileView().as_view(), name="customer_profile"),
]
