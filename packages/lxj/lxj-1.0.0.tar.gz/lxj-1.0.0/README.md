Hello Word!

git clone  https://github.com/kennethreitz/setup.py

python -m pip install --user --upgrade setuptools wheel

python setup.py sdist build
python setup.py bdist_wheel --universal
python setup.py sdist bdist_wheel

pip install twine
twine upload dist/*
