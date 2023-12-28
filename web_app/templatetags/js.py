from django.utils.safestring import mark_safe
from django.template import Library

import json


register = Library()


@register.filter
def js(obj):
    """
    The function `js` converts a Python object to a JSON string and returns it as a safe string.

    :param obj: The `obj` parameter is the object that you want to convert to a JSON string. It can be
    any valid Python object such as a dictionary, list, string, number, boolean, or None
    :return: the JSON representation of the input object, wrapped in a Django `mark_safe` object.
    """
    return mark_safe(json.dumps(obj))
