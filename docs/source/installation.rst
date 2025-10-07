Installation
============

.. rubric:: Basic installation

To install the latest stable release::

    pip3 install treem

To install the development version::

    pip3 install git+https://github.com/a1eko/treem

For alternative installation methods, refer to the official ``pip3`` documentation.


.. rubric:: Dependencies

The ``treem`` module has minimal runtime dependencies:

* Python >= 3.7
* ``matplotlib``
* ``numpy``
* ``PyOpenGL`` (optional, required for the ``swc render`` command)

For testing and documentation purposes, ``treem`` requires the following
development packages and third-party extensions:

* ``sphinx`` with the ``napoleon`` and ``programoutput`` extensions
* ``pytest`` with ``pytest-cov`` plugin
* ``sphinx-rtd-theme``
* ``coverage``
