
treem &ndash; Neuron Morphology Processing Tool
===============================================

The `treem` module (pronounced "trim") provides data structures and
command-line tools for accessing and manipulating digital reconstructions
of neuronal morphology in the Stockley-Wheal-Cannon (SWC) format.

<p>
    <code>    Release</code>
    <sub>
        <sub>
            <a href="https://pypi.org/project/treem/"><img src="https://img.shields.io/pypi/v/treem" alt="PyPI - Version"></a>
            <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.9%20%7C%203.12-blue.svg" alt="Python Versions Tested">
            <a href="https://github.com/a1eko/treem/blob/master/LICENSE"><img src="https://img.shields.io/badge/License-MIT-brightgreen.svg" alt="License: MIT"></a>
        </sub>
    </sub>
    <br>
    <code>  Platforms</code>
        <sub>
            <sub>
                <img src="https://img.shields.io/badge/tested%20on-Linux-fcc624?style=flat&amp;logo=linux&amp;logoColor=white" alt="Linux">
                <img src="https://img.shields.io/badge/tested%20on-macOS-000000?style=flat&amp;logo=apple&amp;logoColor=white" alt="macOS">
                <img src="https://img.shields.io/badge/tested%20on-Windows-0078D4?style=flat&amp;logo=windows&amp;logoColor=white" alt="Windows">
            </sub>
        </sub>
    <br>
    <code>Development</code>
        <sub>
            <sub>
                <a href="https://github.com/a1eko/treem/actions/workflows/build.yml"><img src="https://github.com/a1eko/treem/actions/workflows/build.yml/badge.svg" alt="Build Status"></a>
                <a href="https://sonarcloud.io/dashboard?id=a1eko_treem"><img src="https://sonarcloud.io/api/project_badges/measure?project=a1eko_treem&amp;metric=alert_status" alt="Quality Gate Status"></a>
                <a href="https://codecov.io/gh/a1eko/treem"><img src="https://codecov.io/gh/a1eko/treem/coverage.svg" alt="codecov.io"></a>
                <a href="https://treem.readthedocs.io/en/latest/?badge=latest"><img src="https://readthedocs.org/projects/treem/badge/?version=latest" alt="Documentation Status"></a>
            </sub>
        </sub>
    <br>
    <code>   Citation</code>
        <sub>
            <sub>
                <img src="https://api.juleskreuer.eu/citation-badge.php?doi=10.1007/s12021-021-09531-w" alt="Citation Badge">
                <!-- a href="https://juleskreuer.eu/projects/citation-badge"><img src="https://api.juleskreuer.eu/citation-badge.php?doi=10.1007/s12021-021-09531-w" alt="Citation Badge"></a -->
                <a href="https://doi.org/10.5281/zenodo.4890844"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.4890844.svg" alt="Citation"></a>
            </sub>
        </sub>
</p>

Main classes
------------

Access to morphological data from the source code is provided through the
classes ``Tree``, ``Node``, ``Morph``, and ``SWC``:

* ``Tree``   for recursive tree data structure
* ``Node``   for morphology data storage
* ``Morph``  for neuron morphology representation
* ``SWC``    for definitions of the data format


Commands
--------

Common operations with SWC files can be performed using the ``swc``
command-line tool:

    swc <command> [options] file

Alternatively:

    swc <command> file [file ...] [options] 

List of ``swc`` commands:

* ``check``    tests morphology reconstruction for structural consistency
* ``convert``  converts morphology to compliant SWC format
* ``find``     locates single nodes in the reconstruction
* ``measure``  calculates morphometric features
* ``modify``   manipulates morphology reconstruction
* ``render``   displays 3D model of the reconstruction
* ``repair``   corrects reconstruction errors
* ``view``     shows morphology structure


Installation
------------

Install the latest stable release:

    pip install treem

Install a development version:

    pip install git+https://github.com/a1eko/treem

See also ``pip`` documentation for installation alternatives.


Dependencies
------------

The ``treem`` module has minimal runtime dependencies:

* Python >= 3.7
* ``matplotlib``
* ``numpy``
* ``PyOpenGL`` (optional, enables ``swc render`` command)

For testing and documentation, ``treem`` requires additional development packages with
third-party extensions:

* ``sphinx`` with ``napoleon`` and ``programoutput`` extensions
* ``pytest`` with ``pytest-cov`` plugin
* ``sphinx-rtd-theme``
* ``coverage``


Documentation
-------------

Documentation is available online at [Read the
Docs](https://treem.readthedocs.io/en/latest/).


Citation
--------

* Hjorth JJJ, Hellgren Kotaleski J, Kozlov A (2021) Predicting
Synaptic Connectivity for Large-Scale Microcircuit Simulations
Using Snudda. *Neuroinformatics*, **19**(4):685-701. DOI:
[10.1007/s12021-021-09531-w](https://doi.org/10.1007/s12021-021-09531-w).

* Kozlov AK (2021) Treem - neuron morphology processing tool. *Zenodo*.
DOI: [10.5281/zenodo.4890844](https://doi.org/10.5281/zenodo.4890844).


Funding
-------

Horizon 2020 Framework Programme (785907, HBP SGA2); Horizon 2020
Framework Programme (945539, HBP SGA3); Vetenskapsrådet (VR-M-2017-02806,
VR-M-2020-01652); Swedish e-science Research Center (SeRC); KTH Digital
Futures.

We acknowledge the use of Fenix Infrastructure resources, which are
partially funded from the European Union's Horizon 2020 research and
innovation programme through the ICEI project under the grant agreement
No. 800858.

The computations and testing were enabled by resources provided by the National 
Academic Infrastructure for Supercomputing in Sweden (NAISS), partially funded by 
the Swedish Research Council through grant agreement no. 2022-06725, also by
the Swedish National Infrastructure for Computing (SNIC) at PDC KTH
partially funded by the Swedish Research Council through grant agreement
no. 2018-05973.
