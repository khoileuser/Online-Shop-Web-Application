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


@register.filter
def calc_remain(products_by_vendor):
    """
    The function `calc_remain` calculates the remaining number of products in a given list of vendors.

    :param products_by_vendor: The parameter "products_by_vendor" is a list of dictionaries. Each
    dictionary represents a vendor and contains a key "cart_products" which maps to a list of products
    :return: the total number of products in the "products_by_vendor" list, minus one.
    """
    remain = 0
    for item in products_by_vendor:
        for product in item["cart_products"]:
            remain += 1
    return remain-1


@register.filter
def to_int(value):
    return int(value)
