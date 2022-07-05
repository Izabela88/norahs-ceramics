from django.views.generic import TemplateView
from product.models import Product
from order.models import OrderProduct
from django.db.models import Count


class HomeView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new_arrivals"] = Product.objects.all().order_by(
            "-created_at"
        )[:10]

        context["best_sellers"] = OrderProduct.objects.annotate(
            count=Count("product_id")
        ).order_by("-count")[:3]
        return context
