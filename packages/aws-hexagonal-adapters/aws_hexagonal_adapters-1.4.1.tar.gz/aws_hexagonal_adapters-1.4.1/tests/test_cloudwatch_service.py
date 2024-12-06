import boto3
import pytest

from moto import mock_cloudwatch

from aws_hexagonal_adapters.cloudwatch_service import CloudWatchService

constants = {
    "event_bus_name": "custom_bus",
}


@pytest.fixture(scope="module")
def cloudwatch_client():
    """Fixture to create a mock boto3 CloudWatch client for testing.

    uses the moto mock_cloudwatch context manager to mock CloudWatch.

    yields a boto3 CloudWatch client initialized with:

    - region_name: "us-east-1"

    the mocked client is available to test cases needing a CloudWatch client.
    """

    with mock_cloudwatch():
        yield boto3.client("cloudwatch", region_name="us-east-1")


@pytest.fixture(scope="module")
def cloudwatch_service(cloudwatch_client):
    """Fixture to create a CloudWatchService instance for testing.

    Parameters:
      cloudwatch_client: Fixture that provides a mock boto3 CloudWatch client.

    Create an instance of CloudWatchService with no arguments.

    Yields the CloudWatchService instance to test cases needing a service client.
    """

    yield CloudWatchService()


def test_put_event(cloudwatch_service: CloudWatchService, cloudwatch_client):
    """Tests putting a metric into CloudWatch.

    Parameters:
      cloudwatch_service (CloudWatchService): The service instance to test.
      cloudwatch_client: The mocked boto3 CloudWatch client.

    Call cloudwatch_service.put_metric() to put a test metric into the
    "test" namespace.

    The test metric has:
    - MetricName: "test"
    - Dimensions:
        - Name: "test"
        - Value: "test"
    - Timestamp: "2021-01-01T00:00:00.000Z"
    - Value: 1
    - Unit: "Count"

    Verifies the metric was put successfully.
    """

    cloudwatch_service.put_metric(
        metric=[
            {
                "MetricName": "test",
                "Dimensions": [{"Name": "test", "Value": "test"}],
                "Timestamp": "2021-01-01T00:00:00.000Z",
                "Value": 1,
                "Unit": "Count",
            }
        ],
        name_space="test",
    )
