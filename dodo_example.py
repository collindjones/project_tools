from doit.tools import config_changed
import subprocess
import config
import pandas as pd

last_data = pd.to_datetime('today').strftime('%Y%m%d')
data_exists = config.DATA_DIR.exists()
output_exists = config.OUTPUT_DIR.exists()

def task_create_data():
    return {'actions': ['mkdir _data'], 'uptodate': [data_exists]}
def task_create_output():
    return {'actions': ['mkdir _output'], 'uptodate': [output_exists]}

def task_load_data():
    from project_tools import pullers
    import config
    def pull_data():
        df = pullers.pull_fred('DFF')
        df.to_csv(config.DATA_DIR / 'dff.csv')
    return {'actions': [pull_data], \
            'targets':[config.DATA_DIR / 'dff.csv'], \
            'uptodate':[config_changed(last_data)]}

def task_plot_data():
    from project_tools import plots
    import pandas as pd
    import config
    def plot_data():
        df = pd.read_csv(config.DATA_DIR / 'dff.csv')
        plots.plot(['DFF'], 'DATE', data=df, dates=['DATE'], \
                    output = config.BASE_DIR / '_output', \
                    name='dff', labels = ['Effective Fed Funds'])
    return {'actions': [plot_data], \
            'targets': [config.BASE_DIR / '_output/dff.pdf'], \
            'file_dep': [config.DATA_DIR / 'dff.csv']}

def task_sphinx():
    return {'actions': ['cd docs;make clean html'], \
            'targets':[config.BASE_DIR / 'project_doc.html'], \
            'verbosity': 2}

def task_sphinx_doctest():
    def run_doctests():
        result = subprocess.run(['make', '-C', 'docs', 'doctest'], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
        if result.returncode != 0:
            raise RuntimeError("Doctests failed! See output above.")
    return {'actions': [run_doctests], 'verbosity' : 2, \
            'targets': [config.BASE_DIR / 'build/doctest/output.txt']}
