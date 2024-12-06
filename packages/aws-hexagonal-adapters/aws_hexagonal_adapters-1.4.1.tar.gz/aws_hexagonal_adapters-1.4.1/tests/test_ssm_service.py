import boto3
import pytest

from moto import mock_kms, mock_ssm

from aws_hexagonal_adapters.ssm_service import SSMService

constants = {
    "parameter_name": "hexagonal-adapter/test-parameter",
    "parameter_value": "test-value",
}


@pytest.fixture(scope="module")
def ssm_client():
    """Fixture to create a mock boto3 SSM client for testing.

    uses the moto mock_ssm context manager to mock SSM.

    yields a boto3 SSM client initialized with:

    - region_name: "us-east-1"

    the mocked client is available to test cases needing an SSM client.
    """
    with mock_ssm():
        yield boto3.client("ssm", region_name="us-east-1")


@pytest.fixture(scope="module")
def kms_client():
    """Fixture to create a mock boto3 KMS client for testing.

    uses the moto mock_kms context manager to mock KMS.

    yields a boto3 KMS a client initialized with:

    - region_name: "us-east-1"

    the mocked client is available to test cases needing a KMS client.
    """
    with mock_kms():
        yield boto3.client("kms", region_name="us-east-1")


@pytest.fixture(scope="module")
def ssm_service(ssm_client):
    """Fixture to create an SSMService instance for testing.

    parameters:
      ssm_client: Fixture that provides a mock boto3 SSM client.

    create an instance of SSMService initialized with:

    - region_name: "us-east-1"

    yields the SSMService instance to test cases needing a service client.
    """

    yield SSMService(region_name="us-east-1")


@pytest.fixture(scope="module")
def kms_key(kms_client):
    """Fixture to create a KMS key for testing.

    Parameters:
      kms_client: Fixture that provides a mock boto3 KMS client.

    Use the kms_client to create a KMS key.

    Yields the created KMS key dictionary to test cases needing a KMS key.
    """

    key = kms_client.create_key()
    yield key


@pytest.fixture(scope="module")
def created_ssm_parameter(ssm_service: SSMService, kms_key):
    """Fixture to create an SSM parameter for testing.

    Parameters:
      ssm_service: Fixture that provides SSMService instance.
      kms_key: Fixture that provides KMS key.

    Create an SSM parameter with:

    - Name: constants["parameter_name"]
    - Value: constants["parameter_value"]
    - Description: "test-description"
    - Type: "SecureString"
    - KeyId: kms_key["KeyMetadata"]["KeyId"]

    Yields the created parameter to test cases needing a parameter.
    """

    parameter_name = constants["parameter_name"]
    parameter = ssm_service.create_parameter(
        parameter_name=parameter_name,
        value=constants["parameter_value"],
        description="test-description",
        parameter_type="SecureString",
        key_id=kms_key.get("KeyMetadata", {}).get("KeyId"),
    )
    yield parameter


def test_get_parameter(ssm_service: SSMService, created_ssm_parameter):
    parameter_name = constants["parameter_name"]
    parameter = ssm_service.get_parameter(parameter=parameter_name)
    assert parameter == constants.get("parameter_value")


def test_get_parameters(ssm_service: SSMService, created_ssm_parameter):
    parameter_name = constants["parameter_name"]
    parameters = ssm_service.get_parameters(parameters=[parameter_name])

    assert isinstance(parameters, list)
    assert parameters[0] == constants["parameter_value"]


def test_get_parameters_dict(ssm_service: SSMService, created_ssm_parameter):
    parameter_name = constants["parameter_name"]
    parameters = ssm_service.get_parameters_dict(parameters=[parameter_name])

    assert isinstance(parameters, dict)
    assert parameters[parameter_name] == constants.get("parameter_value")


def test_delete_parameter(ssm_service: SSMService, created_ssm_parameter):
    parameter_name = constants["parameter_name"]
    parameters = ssm_service.delete_parameter(parameter_name=parameter_name)

    assert parameters is None
