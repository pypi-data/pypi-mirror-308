import boto3
import pytest

from moto import mock_sqs

from aws_hexagonal_adapters.sqs_service import SQSService

constants = {
    "queue_name": "queue-name",
    "message_bodies_fifo": [
        {
            "MessageBody": "test message",
            "DelaySeconds": 0,
            "MessageAttributes": {},
            "Id": "test-deduplication-id_1",
            "MessageGroupId": "test-message-group-id",
        },
        {
            "MessageBody": "test message",
            "DelaySeconds": 0,
            "MessageAttributes": {},
            "Id": "test-deduplication-id_2",
            "MessageGroupId": "test-message-group-id",
        },
    ],
    "message_bodies": [
        {
            "MessageBody": "test message",
            "DelaySeconds": 0,
            "MessageAttributes": {},
            "Id": "test-deduplication-id_1",
        },
        {
            "MessageBody": "test message",
            "DelaySeconds": 0,
            "MessageAttributes": {},
            "Id": "test-deduplication-id_2",
        },
    ],
}


@pytest.fixture(scope="module")
def sqs_client():
    """Mock SQS client using moto."""
    with mock_sqs():
        yield boto3.client("sqs", region_name="us-east-1")


@pytest.fixture(scope="module")
def sqs_queue(sqs_client):
    """Create a mock SQS queue."""
    queue_name = constants["queue_name"]
    yield sqs_client.create_queue(QueueName=queue_name)


@pytest.fixture(scope="module")
def sqs_fifo_queue(sqs_client):
    """Create a mock SQS FIFO queue."""
    queue_name = constants["queue_name"]
    fifo_queue_name = f"{queue_name}.fifo"
    yield sqs_client.create_queue(QueueName=fifo_queue_name, Attributes={"FifoQueue": "true"})


@pytest.fixture(scope="module")
def sqs_service(sqs_client):
    """Create a mock SQS queue service."""
    yield SQSService(region_name="us-east-1")


def test_send_message_to_fifo_queue(sqs_fifo_queue, sqs_service):
    """Test sending a message to a FIFO queue."""
    queue_url = sqs_fifo_queue["QueueUrl"]
    message_body = constants["message_bodies_fifo"][0]
    sqs_service.send_message_to_fifo(queue_url=queue_url, message=message_body)


def test_send_message_to_queue(sqs_queue, sqs_service):
    """Test sending a message to a queue."""
    queue_url = sqs_queue["QueueUrl"]
    message_body = constants["message_bodies"][0]
    sqs_service.send_message(queue_url=queue_url, message=message_body)

    # delete messages from the queue
    messages = sqs_service.receive_messages(queue_url=queue_url, max_number_of_messages=1)
    receipt_handle = messages[0]["ReceiptHandle"]
    sqs_service.delete_message(queue_url=queue_url, receipt_handle=receipt_handle)


def test_send_messages_to_queue(sqs_queue, sqs_service):
    """Test sending multiple messages to a queue."""
    queue_url = sqs_queue["QueueUrl"]
    message_bodies = constants["message_bodies"]
    sqs_service.send_messages(queue_url=queue_url, messages=message_bodies)

    # delete two messages from the queue
    messages = sqs_service.receive_messages(queue_url=queue_url, max_number_of_messages=2)
    receipt_handles = [message["ReceiptHandle"] for message in messages]
    for receipt_handle in receipt_handles:
        sqs_service.delete_message(queue_url=queue_url, receipt_handle=receipt_handle)


def test_receive_messages_from_queue(sqs_queue, sqs_service):
    """Test receiving messages from a queue."""
    queue_url = sqs_queue["QueueUrl"]
    sqs_service.send_messages(queue_url=queue_url, messages=constants["message_bodies"])
    messages = sqs_service.receive_messages(queue_url=queue_url, max_number_of_messages=2)
    assert len(messages) == 2
    assert messages[0]["Body"] == constants["message_bodies"][0]["MessageBody"]

    # delete two messages from the queue
    receipt_handles = [message["ReceiptHandle"] for message in messages]
    for receipt_handle in receipt_handles:
        sqs_service.delete_message(queue_url=queue_url, receipt_handle=receipt_handle)


def test_delete_message_from_queue(sqs_queue, sqs_service):
    """Test deleting a message from a queue."""
    queue_url = sqs_queue["QueueUrl"]
    message_body = constants["message_bodies"][0]

    sqs_service.send_message(queue_url=queue_url, message=message_body)

    messages = sqs_service.receive_messages(queue_url=queue_url, max_number_of_messages=1)
    receipt_handle = messages[0]["ReceiptHandle"]
    sqs_service.delete_message(queue_url=queue_url, receipt_handle=receipt_handle)


def test_delete_messages_from_queue(sqs_queue, sqs_service):
    """Test deleting multiple messages from a queue."""
    queue_url = sqs_queue["QueueUrl"]
    sqs_service.send_messages(queue_url=queue_url, messages=constants["message_bodies"])

    messages = sqs_service.receive_messages(queue_url=queue_url, max_number_of_messages=2)
    receipt_handles = [message["ReceiptHandle"] for message in messages]
    for receipt_handle in receipt_handles:
        sqs_service.delete_message(queue_url=queue_url, receipt_handle=receipt_handle)


def test_get_queue_attr(sqs_queue, sqs_service):
    """Test getting queue attributes."""
    queue_url = sqs_queue["QueueUrl"]
    attributes = sqs_service.get_queue_attr(queue_url=queue_url, attribute_names=["ApproximateNumberOfMessages"])
    assert "ApproximateNumberOfMessages" in attributes


def test_queue_has_messages(sqs_queue, sqs_service):
    """Test checking if a queue has messages."""
    queue_url = sqs_queue["QueueUrl"]
    queue_name = constants["queue_name"]
    sqs_service.send_messages(queue_url=queue_url, messages=constants["message_bodies"])
    assert sqs_service.queue_has_messages(queue_name=queue_name)


def test_queue_has_messages_in_flight(sqs_queue, sqs_service):
    """Test checking if a queue has messages in flight."""
    queue_url = sqs_queue["QueueUrl"]
    queue_name = constants["queue_name"]
    sqs_service.send_messages(queue_url=queue_url, messages=constants["message_bodies"])
    messages_in_flight = sqs_service.queue_has_messages_in_flight(queue_name=queue_name)

    assert messages_in_flight is not None
