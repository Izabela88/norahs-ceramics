from django.views.generic import ListView
from product.models import Product

# Create your views here.
class ProductsListView(ListView):
   model = Product
   paginate_by = 4
   context_object_name = "product_list"
   template_name = "product/products-list.html"