from django.views.generic import TemplateView
from product.models import Product


class HomeView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new_arrivals"] = Product.objects.all().order_by(
            "-created_at"
        )[:10]

        return context
