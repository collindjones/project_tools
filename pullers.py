import pandas_datareader.data as web
import json
import urllib
import pandas as pd
import time
import numpy as np
import wrds
import config

cols_keep = [
    'cusip',
    'securityType',
    'interestRate',
    'announcementDate',
    'auctionDate',
    'issueDate',
    'maturityDate',
    'bidToCoverRatio',
    'cashManagementBillCMB',
    'competitiveAccepted',
    'competitiveTendered',
    'corpusCusip',
    'currentlyOutstanding',
    'pdfFilenameSpecialAnnouncement',
    'floatingRate',
    'highDiscountRate',
    'highInvestmentRate',
    'highPrice',
    'highDiscountMargin',
    'highYield',
    'indirectBidderAccepted',
    'indirectBidderTendered',
    'noncompetitiveAccepted',
    'noncompetitiveTendersAccepted',
    'offeringAmount',
    'originalSecurityTerm',
    'securityTerm',
    'primaryDealerAccepted',
    'primaryDealerTendered',
    'reopening',
    'somaAccepted',
    'somaHoldings',
    'somaIncluded',
    'somaTendered',
    'totalAccepted',
    'totalTendered']

def pull_fred(series, start='2001-01-01', end='2099-01-01'):
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

    df = web.DataReader(series, 'fred', start, end)
    return df

def pull_WRDS(lib='', tbl='', sql='', dates=[]):
    """
    Pull a table from WRDS, either by passing lib and tbl or by passing
    a SQL query.

    Parameters
    ----------
    lib : str, default ''
        Library
    tbl: str, default ''
        Table
    sql: str, default ''
        SQL query. Alternative to lib and tbl. If SQL is provided, then
        lib and tbl will be ignored.

    Returns
    -------
    DataFrame
        Result

    Examples
    --------
    # >>> import project_tools.pullers
    # >>> df = project_tools.pullers.pull_WRDS(sql = "WITH yld AS (SELECT caldt, tdnomprc, tdyld, tdduratn, kycrspid FROM crsp_m_treasuries.tfz_dly WHERE caldt = DATE('2025-01-15')) SELECT * FROM yld")
    # Loading library list...
    # Done
    # >>> df.loc[df['kycrspid'] == '20270215.106620', 'tdyld'].values[0]
    # np.float64(0.00010975948313739)
    """

    if (len(lib) == 0 | len(tbl) == 0) and len(sql) == 0:
        raise ValueError("You need to give me either a lib+tbl combo, or a sql query")
    with wrds.Connection(wrds_username=config.WRDS_USERNAME) as db:
        if len(sql) != 0:
            df = db.raw_sql(sql, date_cols=dates)
        else:
            df = db.get_table(library=lib, table=tbl, date_cols=dates)
    return df

def pull_TreasuryDirect_Auctions(types = ['Bill', 'Note', 'Bond', 'FRN', 'TIPS'], cusips=[]):
    """
    Pull auction data from TreasuryDirect.

    Parameters
    ----------
    types: list of strings, default ['Bill', 'Note', 'Bond' 'FRN', 'TIPS'] (all)
        Types of securities to pull auctions for.
    cusips: list of strings, default []
        Cusips to pull auctions for. When this is provided, types is ignored.

    Returns
    -------
    DataFrame
        Result

    Examples
    --------
    >>> import project_tools.pullers
    >>> df = project_tools.pullers.pull_TreasuryDirect_Auctions(cusips=['912810FG8'])
    >>> df.iloc[0]['issueDate']
    Timestamp('1999-02-16 00:00:00')

    """

    data_all = []
    if len(cusips) == 0:
        name = 'type'
        iterator = types
    else:
        name = 'cusip'
        iterator = cusips
    for t in iterator:
        url_dict = {name:t}
        url_built = 'https://www.treasurydirect.gov/TA_WS/securities/search?'
        url_ext = urllib.parse.urlencode(url_dict, doseq=True)
        url_built = url_built + url_ext
        with urllib.request.urlopen(url_built) as url:
            data = json.loads(url.read().decode())
            data_all = data_all + [pd.DataFrame(data)]
            time.sleep(0.5)
    data_all = pd.concat(data_all)
    dates_convert = [
        'issueDate',
        'maturityDate',
        'announcementDate',
        'auctionDate',
        'datedDate',
        'maturingDate',
        'originalIssueDate']
    for c in dates_convert:
        data_all[c] = pd.to_datetime(data_all[c].str[0:10])

    return data_all[cols_keep]
