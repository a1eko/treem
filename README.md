
treem - neuron morphology processing tool
=========================================

Module ``treem`` (prononounced as "trim") provides data structure
and command-line tools for accessing and manipulating the digital
reconstructions of the neuron morphology in Stockley-Wheal-Cannon format
(SWC).

[![PyPI version](https://badge.fury.io/py/treem.svg)](https://badge.fury.io/py/treem)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://github.com/a1eko/treem/blob/master/LICENSE)
![Build Status](https://github.com/a1eko/treem/actions/workflows/python-app.yml/badge.svg)
[![codecov.io](https://codecov.io/gh/a1eko/treem/coverage.svg)](https://codecov.io/gh/a1eko/treem)
[![Documentation Status](https://readthedocs.org/projects/treem/badge/?version=latest)](https://treem.readthedocs.io/en/latest/?badge=latest)
[![Citation](https://zenodo.org/badge/DOI/10.5281/zenodo.4890844.svg)](https://doi.org/10.5281/zenodo.4890844)



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

or sometimes more convenient as

    swc <command> file [file ...] [options] 

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

    pip3 install git+https://github.com/a1eko/treem

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

We acknowledge the use of Fenix Infrastructure resources, which are partially funded from the European Union's Horizon 2020 research and innovation programme through the ICEI project under the grant agreement No. 800858.

The computations and testing were enabled by resources provided by the Swedish National Infrastructure for Computing (SNIC) at PDC KTH partially funded by the Swedish Research Council through grant agreement no. 2018-05973.
