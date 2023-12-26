from django import template

register = template.Library()


@register.filter
def products_price(price, quantity):
    """
    The function calculates the total price of a product given its price and quantity.

    :param price: The price of a single product. It is a numeric value
    :param quantity: The quantity parameter represents the number of products being purchased
    :return: the total price of a product, calculated by multiplying the price by the quantity. The
    result is rounded to two decimal places.
    """
    return round(price * quantity, 2)
