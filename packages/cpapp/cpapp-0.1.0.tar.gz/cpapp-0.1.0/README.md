# cpapp

### Build and upload

1. Install setuptools and wheel (if not already installed):
```bash
pip install setuptools wheel
```

2. Build the package:
```bash
python setup.py sdist bdist_wheel
```

3. Upload the package to PyPI:

First, install `twine` if you haven't:
```bash
pip install twine
```
Then upload the package:
```bash
twine upload dist/*
```
> You'll need a PyPI account to upload your package. If you don't have one, you can create it at pypi.org.


### Install

```bash
pip install cpapp
```
and use it globally:
```bash
cpapp --ext=py
```