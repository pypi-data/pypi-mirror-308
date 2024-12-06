pip install wheel

pip install twine

twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

python3 setup.py sdist bdist_wheel
