New Relic Python Agent Extension Scaffold
=========================================

This repository provides a basic skeleton for creating instrumentation packages
that plug into the Python Agent.

In this example, instrumentation is provided for the `sampleproject
<https://github.com/pypa/sampleproject>`_ from pypa.

Requirements
------------

Loading New Relic python agent extensions relies on the availability of the
``iter_entry_points`` API in `setuptools`_. Therefore, `setuptools`_ must be
available in the application environment.

.. _setuptools: https://setuptools.readthedocs.io/en/latest/pkg_resources.html#convenience-api


Getting Started
---------------

#. Fork this repository, changing the name as appropriate.
#. Modify the `setup.py`_ ``INSTRUMENTED_PACKAGE`` variable to point to the package you are instrumenting.
#. Update the `setup.py`_ ``HOOKS`` variable to add packages and hook functions.

.. _setup.py: setup.py

Testing
-------

All testing can be done through `tox <https://github.com/tox-dev/tox>`_.

.. code-block:: sh

   pip install tox
   tox


Usage
-----

In the application, the extension can be pip installed.

.. code-block:: sh

    pip install newrelic_extension_sampleproject

License
-------

The contents of this repository are licensed under the terms of the
`Apache 2.0 License <https://www.apache.org/licenses/LICENSE-2.0>`_.
