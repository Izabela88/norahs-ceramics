from django.urls import path
from checkout import views


urlpatterns = [
    path("", views.CheckoutView.as_view(), name="checkout"),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    path('success/', views.SuccessView.as_view()), # new
    path('cancelled/', views.CancelledView.as_view()), # new

]
