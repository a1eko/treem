
treem - neuron morphology processing tool
=========================================

Module provides data structure and command-line tools for accessing and
manipulating the digital reconstructions of the neuron morphology in
Stockley-Wheal-Cannon format (SWC).

[![PyPI version](https://badge.fury.io/py/treem.svg)](https://badge.fury.io/py/treem)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://github.com/a1eko/treem/blob/master/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/treem/badge/?version=latest)](https://treem.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/a1eko/treem.svg?branch=master)](https://travis-ci.org/a1eko/treem)
[![Coverage Status](https://coveralls.io/repos/github/a1eko/treem/badge.svg?branch=master&kill_cache=1)](https://coveralls.io/github/a1eko/treem?branch=master)


Main classes
------------

Access to morphological data from the source code is supported by the
classes ``Tree``, ``Node``, ``Morph`` and ``SWC``.

* ``Tree``   - Recursive tree data structure
* ``Node``   - Morphology data storage
* ``Morph``  - Neuron morphology representation
* ``SWC``    - Definitions of the data format


Commands
--------

Common operations with SWC files are possible via the ``swc`` command-line
tool:

    swc <command> [options] file

List of ``swc`` commands:

* ``check``    - Test morphology reconstruction for structural consistency
* ``convert``  - Convert morphology to compliant SWC format
* ``find``     - Locate single nodes in the reconstruction
* ``measure``  - Calculate morphometric features
* ``modify``   - Manipulate morphology reconstruction
* ``render``   - Display 3D model of the reconstruction
* ``repair``   - Correct reconstruction errors
* ``view``     - Show morphology structure


Installation
------------

Install the latest stable release:

    pip3 install treem

Install a development version:

    pip3 install git+git://github.com/a1eko/treem

See also ``pip3`` documentation for installation alternatives.


Dependencies
------------

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


Documentation
-------------

Documentation is available online at [Read the Docs](https://treem.readthedocs.io/en/latest/).


Funding
-------

Horizon 2020 Framework Programme (785907, HBP SGA2); Horizon 2020 Framework Programme (945539, HBP SGA3); Vetenskapsrådet (VR-M-2017-02806, VR-M-2020-01652); Swedish e-science Research Center (SeRC); KTH Digital Futures.

