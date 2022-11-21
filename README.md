# Jupyter Events

[![Build Status](https://github.com/jupyter/jupyter_events/actions/workflows/python-tests.yml/badge.svg?query=branch%3Amain++)](https://github.com/jupyter/jupyter_events/actions/workflows/python-tests.yml/badge.svg?query=branch%3Amain++)
[![codecov](https://codecov.io/gh/jupyter/jupyter_events/branch/main/graph/badge.svg?token=S9WiBg2iL0)](https://codecov.io/gh/jupyter/jupyter_events)
[![Documentation Status](https://readthedocs.org/projects/jupyter-events/badge/?version=latest)](http://jupyter-events.readthedocs.io/en/latest/?badge=latest)

_An event system for Jupyter Applications and extensions._

Jupyter Events enables Jupyter Python Applications (e.g. Jupyter Server, JupyterLab Server, JupyterHub, etc.) to emit **events**—structured data describing things happening inside the application. Other software (e.g. client applications like JupyterLab) can _listen_ and respond to these events.

## Install

Install Jupyter Events directly from PyPI:

```
pip install jupyter_events
```

or conda-forge:

```
conda install -c conda-forge jupyter_events
```

## Documentation

Documentation is available at [jupyter-events.readthedocs.io](https://jupyter-events.readthedocs.io).
