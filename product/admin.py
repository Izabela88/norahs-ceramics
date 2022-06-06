from django.contrib import admin
from product.models import Category, SubCategory, Product, Color


class ProductAdmin(admin.ModelAdmin):
    """
    Admin setting to display list of artwork,
    Ordered by name, with a vertical filter and a
    Search box
    Widget to display image thumbnail in list display
    """

    model = Product
    list_display = (
        "name",
        "slug",
        "price_pence",
        "description",
        "short_description",
        "is_active",
        "is_featured",
        "width_cm",
        "height_cm",
        "length_cm",
        "volume_ml",
        "sub_category",
        "image",
    )


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Color)
