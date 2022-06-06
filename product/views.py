from django.views.generic import ListView, DetailView
from product.models import Product, Color
from product.forms import FilterForm
from django.db.models import Q


class ProductListView(ListView):
    model = Product
    paginate_by = 4
    context_object_name = "product_list"
    template_name = "product/product-list.html"

    def get_queryset(self):
        product_query = Product.objects.filter(is_active=True).all()
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        colors = Color.objects.all()
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

        color_filters = []

        for color in colors:
            if color.name in self.request.GET:
                color_filters.append(Q(colors=color.name))
        if color_filters:
            color_query = color_filters.pop()
            for filter in color_filters:
                color_query |= filter
            product_query = product_query.filter(color_query)

        if sort_by := self.request.GET.get("sort_by"):
            if sort_by == "name_asc":
                product_query = product_query.order_by("name")
            if sort_by == "name_desc":
                product_query = product_query.order_by("-name")
            if sort_by == "price_asc":
                product_query = product_query.order_by("price_pence")
            if sort_by == "price_desc":
                product_query = product_query.order_by("-price_pence")
        return product_query.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = ""
        if sub_category := self.request.GET.get("sub_category"):
            query_params += f"sub_category={sub_category}&"
        if category := self.request.GET.get("category"):
            query_params += f"category={category}&"
        if min_price := self.request.GET.get("min_price"):
            query_params += f"min_price={min_price}&"
        if max_price := self.request.GET.get("max_price"):
            query_params += f"max_price={max_price}&"
        if sort_by := self.request.GET.get("sort_by"):
            query_params += f"sort_by={sort_by}&"

        initials = {
            "category": category,
            "sub_category": sub_category,
            "min_price": min_price,
            "max_price": max_price,
        }
        context["initial_colors"] = []
        colors = Color.objects.all()
        for color in colors:
            if color.name in self.request.GET:
                query_params += f"{color.name}=on&"
                context["initial_colors"].append(color.name)
        context["query_params"] = query_params
        context["filter_form"] = FilterForm(initial=initials)

        return context

    @staticmethod
    def _to_pence(price):
        return price * 100


class ProductDetailView(DetailView):
    model = Product
    template_name = "product/product-details.html"