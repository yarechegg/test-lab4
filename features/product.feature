Feature: Product
  Scenario: Product is available
    Given The base product has availability of 10
    When I check if product is available in amount 5
    Then Product is available

  Scenario: Product availability with zero stock
    Given The base product has availability of 0
    When I check if product is available in amount 1
    Then Product is not available

  Scenario: Product with negative price
    Given A product with price -100
    Then Product is not available