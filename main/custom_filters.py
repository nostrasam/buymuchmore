from django import template

register = template.Library()

@register.filter
def sum_cart_items(cart, attribute):
    return sum(getattr(item, attribute) for item in cart)
