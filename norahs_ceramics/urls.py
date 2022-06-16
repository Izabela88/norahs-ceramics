from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from customer.views import DeleteCustomerProfile

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("accounts/", include("allauth.urls")),
    path("about/", include("about.urls")),
    path("products/", include("product.urls")),
    path("basket/", include("basket.urls")),
    path("customer/", include("customer.urls")),
    path(
        "<int:pk>/delete/",
        DeleteCustomerProfile.as_view(),
        name="customer_delete",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
