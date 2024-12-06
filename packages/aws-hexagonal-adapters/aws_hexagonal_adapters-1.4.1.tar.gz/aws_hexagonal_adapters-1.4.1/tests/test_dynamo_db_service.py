import boto3
import pytest

from boto3.dynamodb.conditions import Attr, Key
from moto import mock_dynamodb

from aws_hexagonal_adapters.dynamo_db_service import DynamoDBService

constants = {"table_name": "test-table", "table_items": [{"id": "1"}, {"id": "2"}]}


@pytest.fixture(scope="module")
def dynamodb_client():
    """Fixture to create a mock boto3 DynamoDB client for testing.

    uses the moto mock_dynamodb context manager to mock DynamoDB.

    yields a boto3 DynamoDB client initialized with:

    - region_name: "us-east-1"

    the mocked client is available to test cases needing a DynamoDB client.
    """
    with mock_dynamodb():
        yield boto3.client("dynamodb", region_name="us-east-1")


@pytest.fixture(scope="module")
def dynamodb_resource():
    """Fixture to create a mock boto3 DynamoDB resource for testing.

    uses the moto mock_dynamodb context manager to mock DynamoDB.

    yields a boto3 DynamoDB resource initialized with:

    - region_name: "us-east-1"

    the mocked resource is available to test cases needing a DynamoDB resource.
    """
    with mock_dynamodb():
        yield boto3.resource("dynamodb", region_name="us-east-1")


@pytest.fixture(scope="module")
def dynamodb_table(dynamodb_resource):
    """Create mock of a dynamodb table."""
    table_name: str = constants.get("table_name")
    table = dynamodb_resource.create_table(
        TableName=table_name,
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    yield table


@pytest.fixture(scope="module")
def dynamodb_service_client(dynamodb_client):
    """Fixture to create a DynamoDBService client for testing.

    parameters:
      dynamodb_client: Fixture that provides a mock boto3 DynamoDB client.

    create an instance of DynamoDBService initialized with:

    - region_name: "us-east-1"

    yields the DynamoDBService instance to test cases needing a service client.
    """

    yield DynamoDBService(region_name="us-east-1")


@pytest.fixture(scope="module")
def dynamodb_service_resource(dynamodb_resource):
    """Fixture to create a DynamoDBService resource for testing.

    parameters:
      dynamodb_resource: Fixture that provides a mock boto3 DynamoDB resource.

    create an instance of DynamoDBService initialized with:

    - region_name: "us-east-1"

    yields the DynamoDBService instance to test cases needing a service resource.
    """

    yield DynamoDBService(region_name="us-east-1")


def test_scan_items(dynamodb_service_client: DynamoDBService, dynamodb_table):
    table_name: str = constants["table_name"]
    result = dynamodb_service_client.scan_items(table_name=table_name)
    assert result is not None
    assert isinstance(result, list)


def test_put_item(dynamodb_service_resource: DynamoDBService, dynamodb_table):
    table_name: str = constants["table_name"]
    table_item: dict = constants["table_items"][0]
    result = dynamodb_service_resource.put_item(table_name=table_name, item=table_item)
    assert result is not None
    assert isinstance(result, dict)


def test_batch_put_items(dynamodb_service_resource: DynamoDBService, dynamodb_table):
    table_name: str = constants["table_name"]
    table_items = constants["table_items"]
    dynamodb_service_resource.batch_put_items(
        table_name=table_name,
        items=table_items,
    )

    result = dynamodb_service_resource.scan_items(table_name=table_name)
    assert result is not None
    assert isinstance(result, list)
    assert len(result) == len(table_items)
    assert all(item in result for item in table_items)


def test_delete_item(dynamodb_service_resource: DynamoDBService, dynamodb_table):
    table_name: str = constants["table_name"]
    table_item: dict = constants["table_items"][0]
    dynamodb_service_resource.put_item(table_name=table_name, item=table_item)
    dynamodb_service_resource.delete_item(table_name=table_name, item=table_item)

    result = dynamodb_service_resource.get_item(table_name=table_name, key=table_item)
    assert result is None


def test_get_item(dynamodb_service_resource: DynamoDBService, dynamodb_table):
    table_name: str = constants["table_name"]
    table_item: dict = constants["table_items"][0]
    dynamodb_service_resource.put_item(table_name=table_name, item=table_item)

    result = dynamodb_service_resource.get_item(table_name=table_name, key=table_item)
    assert result is not None
    assert result == table_item
    assert isinstance(result, dict)


def test_get_items(dynamodb_service_resource: DynamoDBService, dynamodb_table):
    table_name: str = constants["table_name"]
    table_items = constants["table_items"]
    dynamodb_service_resource.batch_put_items(
        table_name=table_name,
        items=table_items,
    )

    filter_expression = Attr("id").eq("1")
    result = dynamodb_service_resource.get_items(table_name=table_name, filter_expression=filter_expression)

    assert result is not None
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == table_items[0]


def test_get_items_page(dynamodb_service_resource: DynamoDBService, dynamodb_table):
    table_name: str = constants["table_name"]
    table_items: list = constants["table_items"]
    dynamodb_service_resource.batch_put_items(
        table_name=table_name,
        items=table_items,
    )

    filter_expression = Attr("id").eq("1")
    result = dynamodb_service_resource.get_items_page(table_name=table_name, filter_expression=filter_expression)

    assert result is not None
    assert isinstance(result["Count"], int)
    assert result["Items"] == [table_items[0]]


def test_query(dynamodb_service_resource: DynamoDBService, dynamodb_table):
    table_name: str = constants["table_name"]
    table_items: list = constants["table_items"]
    dynamodb_service_resource.batch_put_items(
        table_name=table_name,
        items=table_items,
    )

    key_condition_expression = Key("id").eq("1")
    result = dynamodb_service_resource.query(table_name=table_name, KeyConditionExpression=key_condition_expression)

    assert result is not None
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == table_items[0]
