import boto3
import json
from .config import AWS_ENDPOINT_URL, AWS_REGION, SHIPPING_QUEUE

class ShippingPublisher:
    def __init__(self):
        self.client = boto3.client(
            "sqs",
            endpoint_url=AWS_ENDPOINT_URL,
            region_name=AWS_REGION,
            aws_access_key_id="test",
            aws_secret_access_key="test"
        )
        self.queue_url = self.client.get_queue_url(QueueName=SHIPPING_QUEUE)["QueueUrl"]

    def send_shipping_event(self, data):
        self.client.send_message(QueueUrl=self.queue_url, MessageBody=json.dumps(data))

    def poll_shipping(self):
        res = self.client.receive_message(QueueUrl=self.queue_url, MaxNumberOfMessages=10)
        messages = res.get('Messages', [])
        return [json.loads(m['Body'])['shipping_id'] for m in messages]