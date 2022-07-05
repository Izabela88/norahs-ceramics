from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("accounts/", include("allauth.urls")),
    path("about/", include("about.urls")),
    path("products/", include("product.urls")),
    path("basket/", include("basket.urls")),
    path("customers/", include("customer.urls")),
    path("checkout/", include("checkout.urls")),
    path("review/", include("reviews.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
