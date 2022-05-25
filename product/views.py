from django.views.generic import ListView, DetailView
from product.models import Product


class ProductListView(ListView):
   model = Product
   paginate_by = 4
   context_object_name = "product_list"
   template_name = "product/product-list.html"


class ProductDetailView(DetailView):
   model = Product
   template_name = "product/product-details.html"
