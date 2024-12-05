Building Python Packages
11-Nov-2024

https://medium.com/@ebimsv/building-python-packages-07fbfbb959a9

GitHub
https://github.com/Ebimsv/mlpredictor?source=post_page-----07fbfbb959a9--------------------------------


PyCharm
source .venv/bin/activate

pip install .
pip install --upgrade pip

NOTE:
had to manually install pytest
pytest


Publish
pip install twine build

python -m build
Successfully built mlpredictor-0.1.0.tar.gz and mlpredictor-0.1.0-py3-none-any.whl

dist folder w/ following files
.tar.gz
.whl


Upload
twine upload dist/*

COULD NOT get this working!

Follow instructions here
https://pypi.org/manage/account/token

Create API token
touch ~/.pypirc
gedit ~/.pypirc


https://stackoverflow.com/questions/57457879/why-cant-i-upload-my-own-package-to-pypi-when-my-credential-are-working