import factory
from customer import models


class AddressDetailsModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AddressDetails

    id = 1
    address_details_id = None
    address_1 = "34"
    address_2 = "Hathaway Close"
    town = "Bromley"
    postcode = "BR2 8RD"
    county = "Greater London"
    country = "Great Britain"


class UsertModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    id = 1
    phone_number = "07868198007"
    address_details_id = factory.SubFactory(AddressDetailsModelFactory)
