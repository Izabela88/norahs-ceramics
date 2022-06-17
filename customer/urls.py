from django.urls import path
from customer.views import (
    CustomerProfileView,
    CustomerAddressView,
    DeleteCustomerProfile,
    ChangePasswordView,
)

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
    path(
        "<int:pk>/password_change",
        ChangePasswordView.as_view(),
        name="password_change",
    ),
]
