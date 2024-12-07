from scidx.client import NetCDFProcessing, TimeDirection
from datetime import datetime
import numpy as np
import os
import pytest
import random
import string
from . import conftest

SCIDX_ORG=os.environ["SCIDX_ORG"]

def generate_unique_name():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

def test_query_array(client):
    """
    Test registering and querying a netCDF resource
    """
    resource_name = "query_test_" + generate_unique_name()
    netcdf_processing = NetCDFProcessing(group="example_group")
    resource_url="https://raw.githubusercontent.com/sci-ndp/scidx-py/refs/heads/main/tests/data/example.nc"
    source = "test_source_" + generate_unique_name()

    response = client.register_url(
        resource_name = resource_name,
        resource_title="NetCDF Resource Example",
        owner_org=SCIDX_ORG,
        resource_url=resource_url,
        file_type="NetCDF",
        processing=netcdf_processing,
        notes="This is a NetCDF resource for testing.",
        timestamp=datetime.today(),
        extras={"source": source}
    )
    resource_id = response.get("id")
    assert resource_id

    result = client.query_array(
        source = source, 
        var_name = "example", 
        lb = (3, 4), 
        ub = (5,6), 
        timestamp=datetime.today())
    
    assert len(result) == 0

    timestamp = datetime.today().strftime('%Y%m%dT%H%M%S')

    result = client.query_array(
        source = source, 
        var_name = "example", 
        lb = (3,4), 
        ub = (5,6), 
        timestamp=timestamp,
        time_direction=TimeDirection.PAST)
    
    assert len(result) == 1

    (data,_,_) = result[0]
    validation_data = (np.arange(360).reshape((20,18)))[3:6,4:7]
    assert (data == validation_data).all()
    
    delete_response = client.delete_resource(resource_name=resource_name)
    assert delete_response.get("message") == f"{resource_name} deleted successfully"

    
