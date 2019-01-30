
# Publishing

```powershell
python -m pip install --upgrade setuptools wheel twine
python setup.py sdist bdist_wheel

# upload
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

```