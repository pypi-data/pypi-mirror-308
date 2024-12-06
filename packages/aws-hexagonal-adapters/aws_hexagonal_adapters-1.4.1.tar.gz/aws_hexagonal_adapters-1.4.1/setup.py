"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
"""

from setuptools import setup

setup(
    name="aws-hexagonal-adapters",
    version="1.4.1",
    description="Adapters following hexagonal architecture to connect various AWS services.",
    long_description="The idea behind this project is to create secured constructs from the start. \n",
    license="MIT",
    exclude=[
        ".github",
        ".gitignore",
        ".idea",
        ".pre-commit-config.yaml",
        "pyproject.toml",
        "requirements.txt",
        "setup.cfg",
        "ruff.toml",
        "qodana.toml",
        "static-analysis.datadog.yml",
        "/tests",
        "Makefile../Makefile",
    ],
    install_requires=[
        "aws_lambda_powertools>=3.3.0",
        "boto3>=1.35.60",
        "mypy-boto3-cloudwatch>=1.35.0",
        "mypy-boto3-dynamodb>=1.35.60",
        "mypy-boto3-events>=1.35.0",
        "mypy-boto3-s3>=1.35.46",
        "mypy-boto3-ses>=1.35.3",
        "mypy-boto3-sqs>=1.35.0",
        "mypy-boto3-ssm>=1.35.21",
    ],
    python_requires=">=3.11",
)
