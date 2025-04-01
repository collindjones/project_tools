cd "$(dirname "${BASH_SOURCE[0]}")/.."

pwd

mkdir src
touch src/place
mkdir assets
touch assets/place
mkdir data_manual
touch data_manual/place
mkdir reports
mkdir notes
cp project_tools/env.example ./.env
cp project_tools/config_example.py ./config.py
cp project_tools/gitignore_example ./.gitignore
cp project_tools/requirements_example.txt ./requirements.txt
cp project_tools/example.ipynb reports/
cp project_tools/sphinx_tools/example_note_20250312.rst notes/
cp project_tools/dodo_example.py ./dodo.py
cp project_tools/test.py ./src/
cp project_tools/example_yield_curve.ipynb ./reports
cp project_tools/org_test.org notes/

source .env
source project_tools/venv_setup.sh

sphinx-quickstart docs --extensions=sphinx.ext.doctest,sphinx.ext.autodoc,sphinx.ext.autosummary,nbsphinx,sphinx.ext.viewcode
sphinx-build -M html docs/source/ docs/build/
echo "autosummary_generate = True" >> docs/source/conf.py
echo -e "import sys\nimport os\nfrom pathlib import Path\nsys.path.insert(0, str(Path(__file__).resolve().parents[2]))\nsys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))" >> docs/source/conf.py

echo "html_theme_options = {'page_width': '1250px','logo':'bill.png'}" >> docs/source/conf.py

echo -e "Contents \n-------- \n\n.. toctree::\n   :maxdepth: 2\n\n   api\n   reports\n   notes" >> docs/source/index.rst
cp project_tools/sphinx_tools/api.rst docs/source/api.rst
cp project_tools/sphinx_tools/reports.rst docs/source/reports.rst
cp project_tools/sphinx_tools/notes.rst docs/source/notes.rst
mkdir docs/source/_templates/autosummary
cp project_tools/sphinx_tools/module.rst docs/source/_templates/autosummary
ln -s project_tools/bill.png docs/source/_static/

cd docs/source
ln -s ../../reports/ reports
ln -s ../../notes/ notes

cd ..
make clean html
make doctest

cd ..
ln -s docs/build/html/index.html project_doc.html

# Get the absolute path of the script (even if sourced)
script_dir="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

# Get the parent directory of the script
parent_dir="$(dirname "$script_dir")"

# Extract the name of the parent directory
parent_name="$(basename "$parent_dir")"

# Construct the desired path
final_path="$parent_dir/notes/$parent_name.org"

# Echo the path
echo "$final_path"

if [ -n "$AGENDA_LIST_PATH" ]; then
    echo "AGENDA_LIST_PATH is set to: $AGENDA_LIST_PATH"
    touch $AGENDA_LIST_PATH
    echo -e "$final_path" >> $AGENDA_LIST_PATH
    echo -e "#+ARCHIVE: my_custom_archive.org::* Archived Tasks\n* Project Agenda" >> $final_path
fi

cd "$(dirname "${BASH_SOURCE[0]}")/.."
doit

cp project_tools/README_repo.md README.md
git commit -m "Add submodule"
git add .gitignore README.md assets/ config.py data_manual/ docs/ dodo.py notes/example_note_20250312.rst reports/example.ipynb requirements.txt src/
