from django import template

register = template.Library()


def currency(pence):
    pounds = int(pence) / 100
    return '{0:.2f}'.format(pounds)


register.filter("currency", currency)
