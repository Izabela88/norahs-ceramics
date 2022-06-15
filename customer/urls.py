from django.urls import path
from customer.views import CustomerProfileView


urlpatterns = [
    path(
        "customer_profile/<int:id>",
        CustomerProfileView.as_view(),
        name="customer_profile",
    ),
]
