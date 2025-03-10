cd "$(dirname "${BASH_SOURCE[0]}")/.."

pwd

mkdir src
mkdir assets
mkdir data_manual
mkdir reports
mkdir _data
mkdir _output
cp project_tools/env.example ./.env
cp project_tools/config_example.py ./config.py
cp project_tools/gitignore_example ./.gitignore
cp project_tools/requirements_example.txt ./requirements.txt
cp project_tools/example.ipynb reports/

source .env

conda create --prefix $PWD/.venv python
conda activate $PWD/.venv
pip install -r requirements.txt

sphinx-quickstart docs --extensions=sphinx.ext.doctest,sphinx.ext.autodoc,sphinx.ext.autosummary,nbsphinx,sphinx.ext.viewcode
sphinx-build -M html docs/source/ docs/build/
echo "autosummary_generate = True" >> docs/source/conf.py
echo -e "import sys\nimport os\nfrom pathlib import Path\nsys.path.insert(0, str(Path(__file__).resolve().parents[2]))" >> docs/source/conf.py
echo "html_theme_options = {'page_width': '1250px'}" >> docs/source/conf.py

echo -e "Contents \n-------- \n\n.. toctree:: \n api \n reports" >> docs/source/index.rst
cp project_tools/sphinx_tools/api.rst docs/source/api.rst
cp project_tools/sphinx_tools/reports.rst docs/source/reports.rst
mkdir docs/source/_templates/autosummary
cp project_tools/sphinx_tools/module.rst docs/source/_templates/autosummary

cd docs/source
ln -s ../../reports/ reports

cd ..
make clean html
make doctest

cd ..
ln -s docs/build/html/index.html project_doc.html
