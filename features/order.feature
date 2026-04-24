Feature: Order processing
  Scenario: Place order and check stock reduction
    Given The product has availability of 10
    And An empty shopping cart
    When I add product to the cart in amount 5
    And I place an order
    Then The product should have availability of 5