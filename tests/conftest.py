import pytest
import boto3
from services.config import *
from services.db import get_dynamodb_resource


@pytest.fixture(scope="session", autouse=True)
def setup_localstack_resources():
    dynamo_client = boto3.client(
        "dynamodb",
        endpoint_url=AWS_ENDPOINT_URL,
        region_name=AWS_REGION,
        aws_access_key_id="test",
        aws_secret_access_key="test"
    )

    try:
        existing_tables = dynamo_client.list_tables()["TableNames"]
        if SHIPPING_TABLE_NAME not in existing_tables:
            dynamo_client.create_table(
                TableName=SHIPPING_TABLE_NAME,
                KeySchema=[{"AttributeName": "shipping_id", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "shipping_id", "AttributeType": "S"}],
                BillingMode="PAY_PER_REQUEST",
            )

        sqs_client = boto3.client(
            "sqs",
            endpoint_url=AWS_ENDPOINT_URL,
            region_name=AWS_REGION,
            aws_access_key_id="test",
            aws_secret_access_key="test"
        )
        sqs_client.create_queue(QueueName=SHIPPING_QUEUE)
    except Exception as e:
        pytest.skip(f"LocalStack is not available: {e}")

    yield


@pytest.fixture
def dynamo_resource():
    return get_dynamodb_resource()