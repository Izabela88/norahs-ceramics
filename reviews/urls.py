from django.urls import path
from reviews.views import Review


urlpatterns = [
    path(
        "<int:id>/review",
        Review.as_view(),
        name="review",
    ),
]
