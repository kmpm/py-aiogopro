
# Publishing
Check that version is updated in all applicable locations.

```powershell
python -m pip install --upgrade setuptools wheel twine
python setup.py sdist bdist_wheel

# upload to test
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

```