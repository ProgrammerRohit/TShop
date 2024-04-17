from django import template
from math import floor

register = template.Library()

# Create Custom Tag|Function
@register.simple_tag #Anotation
def min_price(tshirt):
    size = tshirt.sizevariant_set.all().order_by().first()
    return size.price

@register.simple_tag #Anotation
def after_discount(tshirt):
    price = min_price(tshirt)
    discount = tshirt.discount
    return floor(price - (price * (discount/100)))

@register.simple_tag #Anotation
def active_button_class(active_size, size):
    if active_size == size:
        return 'dark'
    else:
        return 'light'

@register.simple_tag #Anotation
def multiply(a,b):
    return a*b

@register.simple_tag #Anotation
def calculate_sale_price(price,discount):
    return floor(price - (price * (discount/100)))

@register.simple_tag #Anotation
def get_order_status_class(status):
    if status == 'COMPLETED':
        return 'success'
    else:
        return 'warning'


# Create Custom Filter
@register.filter #Decorator
def cart_payable_amount(cart):
    total = 0
    for c in cart:
        discount = c.get('tshirt').discount
        price = c.get('size').price
        sale_price = calculate_sale_price(price,discount)
        total_of_single_product = sale_price * c.get('quantity')
        total += total_of_single_product
    return total

# Create Custom Filter
@register.filter #Decorator
def rupee(number):
    return f'₹ {number}'