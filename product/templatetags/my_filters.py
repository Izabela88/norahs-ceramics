from django import template

register = template.Library()


def currency(pence):
    return int(pence) / 100


register.filter("currency", currency)
