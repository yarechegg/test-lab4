from behave import given, when, then
from app.eshop import Product, ShoppingCart

@given("The product has availability of {availability}")
def create_product_for_cart(context, availability):
    val = 0 if availability == "None" else int(availability)
    context.product = Product(name="any", price=123, available_amount=val)

@given('An empty shopping cart')
def empty_cart(context):
    context.cart = ShoppingCart()

@when("I add product to the cart in amount {product_amount}")
def add_product(context, product_amount):
    try:
        if product_amount == "None" or int(product_amount) < 0:
            raise ValueError("Invalid amount")
        context.cart.add_product(context.product, int(product_amount))
        context.add_successfully = True
    except (ValueError, TypeError):
        context.add_successfully = False

@then("Product is added to the cart successfully")
def add_successful(context):
    res = getattr(context, 'add_successfully', False)
    assert res is True

@then("Product is not added to cart successfully")
def add_failed(context):
    res = getattr(context, 'add_successfully', False)
    assert res is False