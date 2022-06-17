from django.urls import path
from customer.views import CustomerProfileView, CustomerAddressView
from customer.views import DeleteCustomerProfile

urlpatterns = [
    path(
        "<int:id>",
        CustomerProfileView.as_view(),
        name="customer_profile",
    ),
    path(
        "<int:id>/address",
        CustomerAddressView.as_view(),
        name="customer_address",
    ),
    path(
        "<int:pk>/delete",
        DeleteCustomerProfile.as_view(),
        name="customer_delete",
    ),
]
