from django.views.generic import ListView, DetailView
from product.models import Product


class ProductListView(ListView):
   model = Product
   paginate_by = 4
   context_object_name = "product_list"
   template_name = "product/product-list.html"

   def get_queryset(self):
      product_query = Product.objects.all()
      if sub_category := self.request.GET.get("sub_category"):
         product_query = product_query.filter(sub_category__name=sub_category)
      if category := self.request.GET.get("category"):
         product_query = product_query.filter(sub_category__category_id=category)     
      return product_query


class ProductDetailView(DetailView):
   model = Product
   template_name = "product/product-details.html"
