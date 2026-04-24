import unittest
from app.eshop import Product, ShoppingCart, Order
from unittest.mock import MagicMock


class TestEshop(unittest.TestCase):

    def setUp(self):
        self.product = Product(name='Test Laptop', price=1000.0, available_amount=21)
        self.cart = ShoppingCart()
        self.mock_shipping = MagicMock()

    def tearDown(self):
        self.cart = None
        self.product = None

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Test Laptop')

    def test_product_buy_reduction(self):
        self.product.buy(10)
        self.assertEqual(self.product.available_amount, 11)

    def test_product_equality(self):
        another_product = Product(name='Test Laptop', price=999, available_amount=1)
        self.assertEqual(self.product, another_product)

    def test_cart_initial_total(self):
        self.assertEqual(self.calculate_cart_total(self.cart), 0)

    def test_add_available_amount(self):
        self.cart.add_product(self.product, 11)
        self.assertTrue(self.product in self.cart.products)

    def test_add_non_available_amount(self):
        with self.assertRaises(ValueError):
            self.cart.add_product(self.product, 22)

    def calculate_cart_total(self, cart):
        return sum([p.price * count for p, count in cart.products.items()])

    def test_cart_calculate_total_multiple(self):
        p2 = Product(name='Other', price=50.0, available_amount=5)
        self.cart.add_product(self.product, 1)
        self.cart.add_product(p2, 2)
        self.assertEqual(self.calculate_cart_total(self.cart), 1100.0)

    def test_remove_existing_product(self):
        self.cart.add_product(self.product, 1)
        self.cart.remove_product(self.product)
        self.assertFalse(self.product in self.cart.products)

    def test_mock_add_product(self):
        self.product.is_available = MagicMock(return_value=True)
        self.cart.add_product(self.product, 12345)
        self.product.is_available.assert_called_with(12345)

    def test_place_order_empties_cart(self):
        self.cart.add_product(self.product, 1)
        order = Order(self.cart, self.mock_shipping)
        order.place_order("Самовивіз")
        self.assertEqual(len(self.cart.products), 0)

    def test_order_reduces_stock(self):
        self.cart.add_product(self.product, 5)
        order = Order(self.cart, self.mock_shipping)
        order.place_order("Самовивіз")
        self.assertEqual(self.product.available_amount, 16)


if __name__ == '__main__':
    unittest.main()