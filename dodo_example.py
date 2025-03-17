from doit.tools import config_changed
import subprocess
import config
import pandas as pd
import glob

last_data = pd.to_datetime('today').strftime('%Y%m%d')
data_exists = config.DATA_DIR.exists()
output_exists = config.OUTPUT_DIR.exists()

nodoc = [config.BASE_DIR / 'project_tools/__init__.py', \
         config.BASE_DIR / 'project_tools/dodo_example.py', \
         config.BASE_DIR / 'project_tools/config_example.py']
nodoc = [str(d) for d in nodoc]

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
            'targets':[config.BASE_DIR / 'project_doc.html']}

def task_sphinx_doctest():
    def run_doctests():
        result = subprocess.run(['make', '-C', 'docs', 'doctest'], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
        if result.returncode != 0:
            raise RuntimeError("Doctests failed! See output above.")
    return {'actions': [run_doctests], \
            'targets': [config.BASE_DIR / 'build/doctest/output.txt']}

def task_update_requirements():
    return {'actions': ['pip freeze > requirements.txt'], \
            'targets': [config.BASE_DIR / 'requirements.txt']}

def task_display_notdoc():
    code_extensions = ['.py']
    def find_notdoc():
        docs_generated = glob.glob(str(config.BASE_DIR / 'docs/source/generated/*rst'))
        docs_scripts = []
        for ext in code_extensions:
            docs_scripts = docs_scripts + glob.glob(str(config.BASE_DIR / '**/*.py'))

        docs_generated = [d.split('/')[-1].split('.')[-2] for d in docs_generated]
        docs_scripts = [d for d in docs_scripts if not d in nodoc]
        docs_scripts = [d.split('/')[-1].split('.')[-2] for d in docs_scripts]

        notdoc = [d for d in docs_scripts if not d in docs_generated]

        print('\n\nScripts not appearing in API:\n------------------------------')
        for f in notdoc:
            print(f + '\n')
        if len(notdoc) == 0:
            print('None!\n')
        print('------------------------------')

    return {'actions':[find_notdoc], 'verbosity':2}
