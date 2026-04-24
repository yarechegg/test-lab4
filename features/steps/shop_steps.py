from behave import when, then


@when('I place an order')
def step_place_order(context):
    from app.eshop import Order
    context.order = Order(context.cart)
    context.order.place_order()

@then('The product should have availability of {expected_amount}')
def step_check_final_stock(context, expected_amount):
    assert context.product.available_amount == int(expected_amount)