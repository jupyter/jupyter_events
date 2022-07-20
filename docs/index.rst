.. jupyter_events documentation master file, created by
   sphinx-quickstart on Fri Sep 27 16:34:00 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Jupyter Events
==============

**Configurable event system for Jupyter applications and extensions.**


Jupyter Events provides a configurable traitlets object, EventLogger,
for structured event-logging in Python. It leverages Python's
standard logging library for filtering, handling, and recording
events. All events are validated (using jsonschema) against
registered JSON schemas.

The most common way to use Jupyter's event system is to configure
the ``EventLogger`` objects in Jupyter Applications,
(e.g. JupyterLab, Jupyter Notebook, JupyterHub). See the
page ":ref:`using-events`"

If you're looking to add events to an application that
you're developing, check out the page ":ref:`adding-events`"



Installation
------------

Jupyter's Events library can be installed from PyPI.

.. code-block::

    pip install jupyter_events


.. toctree::
   :maxdepth: 1
   :caption: Table of Contents:

   pages/configure
   pages/application
   pages/schemas
   pages/redaction_policies
   pages/demo

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
