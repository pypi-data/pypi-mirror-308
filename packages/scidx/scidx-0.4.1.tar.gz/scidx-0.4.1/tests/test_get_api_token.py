import os
import pytest
from requests.exceptions import HTTPError
from . import conftest

SCIDX_USER=os.environ["SCIDX_USER"]
SCIDX_PASSWORD=os.environ["SCIDX_PASSWORD"]

# Test for successfully retrieving an API token
def test_get_api_token_success(client):
    """
    Test that the get_api_token function correctly retrieves an 
    access token when the authentication is successful.
    """
    # Call the get_api_token method with the real credentials
    token = client.get_api_token(username=SCIDX_USER, password=SCIDX_PASSWORD)
    
    # Check that the token is not None or empty
    assert token is not None
    assert len(token) > 0

# Test for failed API token retrieval due to incorrect credentials
def test_get_api_token_failure(client):
    """
    Test that the get_api_token function raises an HTTPError when 
    the authentication fails due to incorrect credentials.
    """
    # Attempt to retrieve the token with incorrect credentials
    with pytest.raises(HTTPError) as exc_info:
        client.get_api_token(username="wrong_user", password="wrong_password")
    
    # Check that the exception is indeed an HTTPError
    assert isinstance(exc_info.value, HTTPError)
    
    # Check that the status code in the error is 401 (Unauthorized)
    assert exc_info.value.response.status_code == 401
    
    # Check that the exception message contains 'Unauthorized'
    assert "Unauthorized" in str(exc_info.value)
