import pandas_datareader.data as web
import pandas as pd
import numpy as np
import wrds

def pull_fred(series, start='2001-01-01'):
    """
    Pull a series from FRED.

    Parameters
    ----------
    series : str
        Series to pull. Easiest way to find this is to go to the FRED website and copy.
    start : str, default '2001-01-01'
        Start date.

    Returns
    -------
    DataFrame
        Result. With DATE as index.


    Examples
    --------
    >>> import project_tools.pullers
    >>> df = project_tools.pullers.pull_fred('DFF')
    >>> df.iloc[0]
    DFF    5.41
    Name: 2001-01-01 00:00:00, dtype: float64

    """

    df = web.DataReader(series, 'fred', start, 'today')
    return df
