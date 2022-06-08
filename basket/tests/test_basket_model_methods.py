import pytest
from basket.tests import factories
from product.tests.factories import ProductModelFactory, CategoryModelFactory, SubCategoryModelFactory
from basket.models import BasketProduct


@pytest.fixture
def sub_category():
    category = CategoryModelFactory()
    sub_category = SubCategoryModelFactory(category=category)
    return sub_category

@pytest.mark.django_db
def test_add_product_method(sub_category):
    basket = factories.BasketModelFactory()
    product = ProductModelFactory(sub_category=sub_category)
    basket.add_product(product.id)
    basket_products = BasketProduct.objects.all()
    assert len(basket_products) == 1
    assert str(basket_products[0].basket_id) == basket.id
    assert basket_products[0].product_id == product.id


@pytest.mark.django_db
def test_subtract_product_method(sub_category):
    basket = factories.BasketModelFactory()
    product = ProductModelFactory(sub_category=sub_category)
    BasketProduct(product_id=product.id, basket_id=basket.id).save()
    basket.subtract_product(product.id)
    basket_products = BasketProduct.objects.all()
    assert len(basket_products) == 0 
  