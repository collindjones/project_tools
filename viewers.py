import pandas as pd
from tabulate import tabulate
import config
import subprocess

def display_org(df):
    """
    Display a pandas dataframe in emacs org-mode, in same ipython session

    Parameters
    ----------
    df : pandas DataFrame

    Returns
    -------
    Nothing

    Examples
    --------
    See example in viewers.py script. Not good for docstring.

    """
    df_org = tabulate(df, headers="keys", tablefmt="orgtbl")

    with open(config.DATA_DIR / 'org_disp_tmp.org', 'w') as f:
        f.write(df_org)

    subprocess.call(['emacs', str(config.DATA_DIR / 'org_disp_tmp.org')])
    subprocess.call(['rm', str(config.DATA_DIR / 'org_disp_tmp.org')])
    subprocess.call(['rm', '-f', str(config.DATA_DIR / '.#org_disp_tmp.org')])
    subprocess.call(['rm', '-f', str(config.DATA_DIR / '#org_disp_tmp.org#')])

if __name__ == '__main__':
    df = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')
    display_org(df.head(30))
