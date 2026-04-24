import uuid
from .repository import ShippingRepository
from .publisher import ShippingPublisher


class ShippingService:
    def __init__(self, repo=None, pub=None):
        self.repo = repo or ShippingRepository()
        self.pub = pub or ShippingPublisher()

    def create_shipping(self, type, products, order_id, due_date):
        available_types = ["Нова Пошта", "Укр Пошта", "Самовивіз"]
        if type not in available_types:
            raise ValueError("Shipping type is not available")

        ship_id = str(uuid.uuid4())
        self.repo.create_shipping(ship_id, type, products, order_id, "created", due_date)
        self.pub.send_shipping_event({"shipping_id": ship_id, "status": "created"})
        return ship_id

    def check_status(self, shipping_id):
        data = self.repo.get_shipping(shipping_id)
        return 'in progress' if data else None