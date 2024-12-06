import boto3
import pytest

from moto import mock_events

from aws_hexagonal_adapters.event_bridge_service import EventsService

constants = {
    "event_bus_name": "custom_bus",
}


@pytest.fixture(scope="module")
def events_client():
    """Fixture to create a mock boto3 EventBridge client for testing.

    Uses the moto mock_events context manager to mock EventBridge.

    Yields a boto3 EventBridge client initialized with:

    - region_name: "us-east-1"

    The mocked client is available to test cases needing an EventBridge client.
    """
    with mock_events():
        yield boto3.client("events", region_name="us-east-1")


@pytest.fixture(scope="module")
def events_service(events_client):
    """Fixture to create an EventsService instance for testing.

    Parameters:
      events_client: Fixture that provides a mock boto3 EventBridge client.

    Creates an instance of EventsService initialized with:

    - region_name: "us-east-1"
    - event_bus_name: constants["event_bus_name"]

    Yields the EventsService instance to test cases needing a service client.
    """

    yield EventsService(region_name="us-east-1", event_bus_name=constants["event_bus_name"])


def test_put_event(events_service: EventsService, events_client):
    events_service.put_event(item={"Source": "test", "EventBusName": constants["event_bus_name"]})
