from datetime import datetime
from dateutil import parser
from enum import Enum
import json
from typing import Optional

try:
    from dxspaces import DXSpacesClient
except ImportError:
    DXSpacesClient = None
from .search_resource import search_resource

class TimeDirection(Enum):
    FUTURE = 1
    PAST = 2

    def __str__(self):
        if self == TimeDirection.FUTURE:
            return(">")
        else:
            return("<")

class StagingFailure(Exception):
    pass

_excluded_extras = ['staging_handle', 'staging_socket']

def _time_arg_to_str(arg):
    if isinstance(arg, str):
        time = parser.isoparse(arg)
    elif isinstance(arg, datetime):
        time = arg
    else:
        raise ValueError("timestamp must be a datetime or a parseable datetime string")
    return(time.strftime('%Y-%m-%dT%H:%M:%S'))

def _get_query_time_string(**kwargs):
    if 'timestamp' in kwargs:
        tstamp_str = _time_arg_to_str(kwargs['timestamp'])
        tstamp_direction = TimeDirection.FUTURE
        if 'time_direction' in kwargs:
            if not isinstance(kwargs['time_direction'], TimeDirection):
                raise ValueError("time_direction should be FUTURE or PAST")
            tstamp_direction = kwargs['time_direction']
        return(f'{tstamp_direction}{tstamp_str}')
    time_string = None
    if 'start_time' in kwargs:
        time_string = _time_arg_to_str(kwargs['start_time']) + '/'
    if 'end_time' in kwargs:
        end_time_string = _time_arg_to_str(kwargs['end_time'])
        if time_string:
            time_string = time_string + end_time_string
        else:
            time_string = '/' + end_time_string
    return(time_string)

def _get_data_from_staging(staging_handle: str, var_name: str, staging_socket: str, lb: tuple[int], ub: tuple[int], timestamp: str, **kwargs):
    staging_handle = json.loads(staging_handle)
    namespace = None
    if 'namespace' in staging_handle:
        namespace = staging_handle['namespace']
        del staging_handle['namespace']
    name = 'var_name:' + var_name
    if 'parameters' in staging_handle:
        params = staging_handle['parameters']
        for p in params:
            name = name + f',{p}:{params[p]}'
    client = DXSpacesClient(staging_socket)
    data = client.GetNDArray(name=name, version=0, lb=lb, ub=ub, namespace=namespace)
    if data is None:
        raise StagingFailure("registered data not found in staging.")
    return(data, parser.isoparse(timestamp))

def query_array(self, source: str,  var_name: str, lb: tuple[int], ub: tuple[int], dataset_name: Optional[str] = None, dataset_title: Optional[str] = None,
            owner_org: Optional[str] = None, **kwargs) -> list[tuple]:
    """
    Download a subset of an array within a dataset previously registered as external data with sciDX.

    Parameters
    ----------
    source : str
        The name of the external source.
    var_name : str
        The name of the array to access.
    lb : tuple[int]
        The lower-bounds of array indices to access.
    ub : tuple[int]
        The upper-bounds of array indices to access.
    dataset_name : str, optional
        The name of the dataset.
    dataset_title : str, optional
        The title of the dataset.
    owner_org : str, optional
        The ID of the organization
    timestamp : str or datetime, optional
        Find a result nearest in time to the given timestamp.
    time_direction : TimeDirection
        Either `TimeDirection.FUTURE` or `TimeDirection.PAST`. If the former, and `timestamp` is given, then "nearest in time" looks forward in time; if the latter, backwards. Default behavior is forward-looking.
    start_time : str or datetime, optional
        The start of a time interval, which stretches to the infinite future if end_time is not given
    end_time: str or datetime, optional
        The end of a time interval, which stretches to the infinite past if start_time is not given.

    Returns
    -------
    list[Tuple[NDArray, datetime, dict]]
        A list of tuples, one per matching dataset. Each tuple consists of the matching subset, the timestamp of the dataset or None, and a metadata dict for the dataset.
    
    Raises
    ------
    Exception
        If the query fails for any reason other than no results found.
    """
    if not DXSpacesClient:
        raise NotImplementedError("querying requires beta staging support. Please build scidx[staging].")
    if not len(lb) == len(ub):
        raise 
    time_string = _get_query_time_string(**kwargs)
    filter_list = [f'source:{source}']
    search_results = self.search_resource(dataset_name, dataset_title, owner_org, timestamp=time_string, filter_list=filter_list)
    results = []
    for result in search_results:
        if 'extras' in result:
            extras = result['extras']
            if 'staging_handle' in extras and 'staging_socket' in extras:
                data, timestamp = _get_data_from_staging(lb=lb, ub=ub, var_name=var_name, **extras)
                for extra in _excluded_extras:
                    if extra in extras:
                        del extras[extra]
                results.append((data, timestamp, extras))
    return(results)
                

    
