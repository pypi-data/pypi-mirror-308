import os
import pytest
from scidx.client import sciDXClient

SCIDX_SOCKET=os.environ["SCIDX_SOCKET"]
SCIDX_ORG=os.environ["SCIDX_ORG"]
SCIDX_USER=os.environ["SCIDX_USER"]
SCIDX_PASSWORD=os.environ["SCIDX_PASSWORD"]

@pytest.fixture(scope="module")
def client():
    """
    Fixture to create and login the client for testing.
    """
    client = sciDXClient(SCIDX_SOCKET)
    client.login(SCIDX_USER, SCIDX_PASSWORD)
    return client
