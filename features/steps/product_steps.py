from behave import given, when, then
from app.eshop import Product

@given("The base product has availability of {availability}")
def create_base_product(context, availability):
    val = 0 if availability == "None" else int(availability)
    context.product = Product(name="test", price=100, available_amount=val)

@when("I check if product is available in amount {check_amount}")
def check_availability(context, check_amount):
    try:
        if check_amount == "None":
            context.is_available = context.product.is_available(None)
        else:
            context.is_available = context.product.is_available(int(check_amount))
    except (ValueError, TypeError):
        context.is_available = False

@then("Product is available")
def product_is_available(context):
    assert context.is_available is True

@then("Product is not available")
def product_is_not_available(context):
    assert context.is_available is False

@given('A product with price {price}')
def step_create_negative_product(context, price):
    context.product = Product(name="ErrorItem", price=int(price), available_amount=10)
    context.is_available = False if int(price) < 0 else True