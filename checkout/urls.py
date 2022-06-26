from django.urls import path
from checkout import views


urlpatterns = [
    path("", views.CheckoutView.as_view(), name="checkout"),
    path(
        "create_checkout_session/",
        views.create_checkout_session,
        name="checkout_session",
    ),
    path("success/", views.SuccessView.as_view()),  # new
    path("", views.CancelledView.as_view()),  # new
    path("payment_webhook", views.my_webhook_view),  # new
]
