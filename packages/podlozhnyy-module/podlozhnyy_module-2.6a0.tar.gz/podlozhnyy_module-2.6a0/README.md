# podlozhnyy-module

A set of tools to simplify data analysis in particular:
 - risk analytics package
 - statistical utils for AB testing, analysis of correlations and variance
 - bootstrap method and permutations criteria for non-parametric testing
 - time series analysis and forecasting
 - classical machine learning

### Getting started

Easy installation via `pip`

```
$ pip install podlozhnyy-module
```

### For developers

If you would like to contribute to the project yo can do the following

1. Create a new virtual environment and activate it (_for Windows use: `my_env\Scripts\activate` instead of the last command_)
```
$ python -m venv my_env
$ source my_env/bin/activate
```

2. Copy the repo
```
$ git clone https://github.com/NPodlozhniy/podlozhnyy-module.git
```

3. Install requirement dependecies for developers
```
$ pip install -r requirements_dev.txt
```

4. Make changes and then release version to PyPI (use `--repository-url` argument to upload code to test PyPI version)
```
$ python setup.py sdist bdist_wheel
$ twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

:heavy_exclamation_mark: Important Update :heavy_exclamation_mark: since 2024 PyPi doesn't allow to push without API token, so you need to [create](https://pypi.org/help/#apitoken) one and then push using either `.pypirc` file, what actually doesn't work for me, or specifying credentials during the call

```
$ twine upload --repository-url https://test.pypi.org/legacy/ dist/* -u __token__ -p <YOUR TOKEN>
```

5. To test the package create another virtual environment and then install library from PyPI using the following command
```
$ pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple podlozhnyy-module
```
