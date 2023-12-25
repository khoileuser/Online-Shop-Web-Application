from django import template

register = template.Library()


@register.filter
def products_price(price, quantity):
    return round(price * quantity, 2)
