Installation
============

.. rubric:: Basic installation

Install the latest stable release::

    pip3 install treem

Install a development version::

    pip3 install git+git://github.com/a1eko/treem

See also  ``pip3`` documentation for installation alternatives.


.. rubric:: Dependencies

Module ``treem`` has minimal runtime dependencies:

* ``python`` >= 3.7
* ``matplotlib``
* ``numpy``
* ``PyOpenGL`` (optional) enables ``swc render`` command

For testing and documentation, ``treem`` needs development packages with
third-party extensions:

* ``sphinx`` with ``napoleon`` and ``programoutput``
* ``pytest`` with ``pytest-cov``
* ``coverage``

