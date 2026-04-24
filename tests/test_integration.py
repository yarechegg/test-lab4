import pytest
import uuid
from app.eshop import Product, ShoppingCart, Order
from services.service import ShippingService
from services.repository import ShippingRepository
from services.publisher import ShippingPublisher
from datetime import datetime, timedelta, timezone

# 1. Базовий тест логіки (Mocker)
def test_place_order_logic(mocker):
    mock_repo = mocker.Mock()
    mock_pub = mocker.Mock()
    service = ShippingService(mock_repo, mock_pub)
    order = Order(ShoppingCart(), service, "order_123")
    result = order.place_order("Нова Пошта")
    assert isinstance(result, str)
    assert mock_repo.create_shipping.called

# 2. Тест валідації типу доставки
def test_invalid_shipping_type(dynamo_resource):
    service = ShippingService(ShippingRepository(), ShippingPublisher())
    with pytest.raises(ValueError, match="Shipping type is not available"):
        service.create_shipping("Кур'єр на голубів", [], "o1", datetime.now(timezone.utc))

# 3. Тест інтеграції з SQS (Черга)
def test_sqs_integration(dynamo_resource):
    service = ShippingService(ShippingRepository(), ShippingPublisher())
    ship_id = service.create_shipping("Укр Пошта", ["p1"], "o1", datetime.now(timezone.utc))
    pub = ShippingPublisher()
    assert ship_id in pub.poll_shipping()

# 4. Тест синхронізації залишків на складі
def test_order_inventory_sync(dynamo_resource):
    service = ShippingService(ShippingRepository(), ShippingPublisher())
    prod = Product(name="SyncTest", price=10, available_amount=5)
    cart = ShoppingCart()
    cart.add_product(prod, 2)
    order = Order(cart, service)
    order.place_order("Нова Пошта")
    assert prod.available_amount == 3

# 5. Тест перевірки статусу в DynamoDB
def test_check_status_integration(dynamo_resource):
    service = ShippingService(ShippingRepository(), ShippingPublisher())
    ship_id = service.create_shipping("Самовивіз", ["p1"], "o1", datetime.now(timezone.utc))
    assert service.check_status(ship_id) == 'in progress'

# 6. Тест очищення кошика після замовлення
def test_cart_empties_after_order(dynamo_resource):
    service = ShippingService(ShippingRepository(), ShippingPublisher())
    cart = ShoppingCart()
    cart.add_product(Product("P1", 10, 10), 1)
    order = Order(cart, service)
    order.place_order("Нова Пошта")
    assert len(cart.products) == 0

# 7. Тест замовлення кількох різних товарів
def test_multiple_products_order(dynamo_resource):
    service = ShippingService(ShippingRepository(), ShippingPublisher())
    p1 = Product("Apple", 10, 10)
    p2 = Product("Orange", 20, 10)
    cart = ShoppingCart()
    cart.add_product(p1, 2)
    cart.add_product(p2, 3)
    order = Order(cart, service)
    ship_id = order.place_order("Нова Пошта")
    repo = ShippingRepository()
    ship_data = repo.get_shipping(ship_id)
    assert "Apple" in ship_data['product_ids']
    assert "Orange" in ship_data['product_ids']

# 8. Тест видалення товару перед оформленням
def test_remove_product_before_order(dynamo_resource):
    service = ShippingService(ShippingRepository(), ShippingPublisher())
    p1 = Product("DeleteMe", 100, 5)
    cart = ShoppingCart()
    cart.add_product(p1, 1)
    cart.remove_product(p1)
    order = Order(cart, service)
    ship_id = order.place_order("Самовивіз")
    repo = ShippingRepository()
    ship_data = repo.get_shipping(ship_id)
    assert ship_data['product_ids'] == ""

# 9. Тест граничного залишку (купівля всього складу)
def test_buy_full_stock(dynamo_resource):
    service = ShippingService(ShippingRepository(), ShippingPublisher())
    prod = Product("LastItem", 50, 1)
    cart = ShoppingCart()
    cart.add_product(prod, 1)
    order = Order(cart, service)
    order.place_order("Укр Пошта")
    assert prod.available_amount == 0

# 10. Тест повторного використання сервісу для різних замовлень
def test_service_reuse_for_multiple_orders(dynamo_resource):
    service = ShippingService(ShippingRepository(), ShippingPublisher())
    id1 = service.create_shipping("Нова Пошта", ["item1"], "o1", datetime.now(timezone.utc))
    id2 = service.create_shipping("Укр Пошта", ["item2"], "o2", datetime.now(timezone.utc))
    assert id1 != id2