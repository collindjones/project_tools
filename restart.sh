cd "$(dirname "${BASH_SOURCE[0]}")/.."

pwd

rm -r src
rm -r assets
rm -r data_manual
rm -r reports
rm -r docs
rm -r _output
rm -r _data
rm -r notes
rm project_doc.html
find ./ -maxdepth 1 -type f -exec rm {} \;

conda deactivate
conda env remove -p $PWD/.venv
