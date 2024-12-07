import requests


def delete_resource(self, resource_name: str = None, resource_id: str = None) -> dict:
    """
    Delete a resource in the sciDX system.

    Parameters
    ----------
    resource_name : str
        The name of the resource to be deleted.
    resource_id : str
        The id of the resource to be deleted.

    Returns
    -------
    dict
        A dictionary containing the response from the API.

    Raises
    ------
    HTTPError
        If the API request fails with detailed error information.
    """
    if bool(resource_name) == bool(resource_id):
        raise ValueError("exactly one of resource_name and resource_id must not be None")

    
    # Define the URL for the DELETE request using the resource_name or resource_id
    url = f"{self.api_url}/resource"
    if resource_name:
        url = url + f"/{resource_name}"
  
    # Set parameters (either resource_id or nothing)
    params = {}
    if resource_id:
        params["resource_id"] = resource_id
    
    # Get headers for authorization or other needed parameters
    headers = self._get_headers()

    # Make the DELETE request to the API
    response = requests.delete(url, headers=headers, params=params)
    
    # If the response is successful, return the confirmation message
    if response.status_code == 200:
        return response.json()
    # If the resource is not found, raise an HTTPError with a detailed message
    elif response.status_code == 404:
        raise requests.exceptions.HTTPError(
            f"Resource '{resource_name}' not found.", 
            response=response
        )
    # For other cases, raise an HTTPError with a detailed message
    else:
        error_message = (
            f"Failed to delete resource '{resource_name}'. "
            f"Request URL: {url}\n"
            f"Response Status Code: {response.status_code}\n"
            f"Response Content: {response.content.decode('utf-8')}"
        )
        raise requests.exceptions.HTTPError(error_message, response=response)
