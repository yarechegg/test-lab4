from .db import get_dynamodb_resource
from .config import SHIPPING_TABLE_NAME

class ShippingRepository:
    def __init__(self):
        self.table = get_dynamodb_resource().Table(SHIPPING_TABLE_NAME)

    def create_shipping(self, shipping_id, type, products, order_id, status, due_date):
        self.table.put_item(Item={
            'shipping_id': shipping_id,
            'type': type,
            'product_ids': ",".join(products) if isinstance(products, list) else products,
            'order_id': order_id,
            'status': status,
            'due_date': str(due_date)
        })
        return shipping_id

    def get_shipping(self, shipping_id):
        res = self.table.get_item(Key={'shipping_id': shipping_id})
        return res.get('Item')