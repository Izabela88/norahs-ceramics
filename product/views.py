from django.views.generic import ListView, DetailView
from product.models import Product
from product.forms import FilterForm


class ProductListView(ListView):
    model = Product
    paginate_by = 4
    context_object_name = "product_list"
    template_name = "product/product-list.html"

    def get_queryset(self):
        product_query = Product.objects.all()
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")

        if sub_category := self.request.GET.get("sub_category"):
            product_query = product_query.filter(
                sub_category__name=sub_category
            )
        if category := self.request.GET.get("category"):
            product_query = product_query.filter(
                sub_category__category_id=category
            )
        if min_price and max_price:
            product_query = product_query.filter(
                price_pence__range=(
                    self._to_pence(int(min_price)),
                    self._to_pence(int(max_price)),
                )
            )
        return product_query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = ""
        if sub_category := self.request.GET.get("sub_category"):
            query_params += f"sub_category={sub_category}"
        if category := self.request.GET.get("category"):
            query_params += f"category={category}"
        if min_price := self.request.GET.get("min_price"):
            query_params += f"min_price={min_price}"
        if max_price := self.request.GET.get("max_price"):
            query_params += f"max_price={max_price}"
        context["query_params"] = query_params
        context["filter_form"] = FilterForm(
            initial={"category": category, "sub_category": sub_category}
        )
        return context

    @staticmethod
    def _to_pence(price):
        return price * 100


class ProductDetailView(DetailView):
    model = Product
    template_name = "product/product-details.html"