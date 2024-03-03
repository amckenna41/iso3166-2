# Documentation for iso3166-2

[![Documentation Status](https://readthedocs.org/projects/iso3166-2/badge/?version=latest)](https://iso3166-2.readthedocs.io/en/latest/?badge=latest)

The documentation for `iso3166-2` is hosted on the **readthedocs** platform and is available [here](https://iso3166-2.readthedocs.io/en/latest). The documentation is automatically built and published on the platform via the repo. 

## Build documentation and test locally

Install *sphinx* Python package
```bash
pip install sphinx
```

Create a /docs directory inside the `iso3166-2` package
```bash
mkdir /docs
```

Run *sphinx-quickstart* in /docs directory to create template for the documentation
```bash
cd /docs && sphinx-quickstart
```

After editing the documentation, build using make command in the /docs folder
```bash
make html 
```

Open the index.html file generated in the docs/_build/html folder
```bash
open _build/html/index.html
```

The full tutorial for using the readthedocs platform is available [here](https://docs.readthedocs.io/en/stable/tutorial/index.html).
