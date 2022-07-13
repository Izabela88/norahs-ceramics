from django.contrib.sitemaps import Sitemap
from product.models import Product
from django.urls import reverse


class Product_Sitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class Static_Sitemap(Sitemap):

    priority = 1.0
    changefreq = "daily"

    def items(self):
        return ["about", "home"]

    def location(self, item):
        return reverse(item)
