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

* ``python`` >= 3.7
* ``matplotlib``
* ``numpy``
* ``PyOpenGL`` optional, enables ``swc render`` command

For testing and documentation purposes, ``treem`` requires additional development packages with third-party support:

* ``sphinx`` with ``napoleon`` and ``programoutput`` extensions
* ``sphinx-rtd-theme``
* ``pytest`` with optional ``pytest-cov`` plugin
* ``coverage``
