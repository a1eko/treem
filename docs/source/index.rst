
treem - neuron morphology processing tool
=========================================


.. rubric:: Module ``treem``

Module provides data structure and command-line tools for accessing and
manipulating the digital reconstructions of the neuron morphology in
Stockley-Wheal-Cannon format (SWC).


.. rubric:: Main classes

Access to morphological data from the source code is supported by the
classes ``Tree``, ``Node``, ``Morph`` and ``SWC``.

=========  =========================================================
``Tree``   Recursive tree data structure
``Node``   Morphology data storage
``Morph``  Neuron morphology representation
``SWC``    Definitions of the data format
=========  =========================================================

For the complete list of available functions, see :ref:`api:API
reference`.


.. rubric:: Commands

Common operations with SWC files are possible via the ``swc`` command-line
tool::

    swc <command> [options] file

List of ``swc`` commands:

=========  =========================================================
`check`    Test morphology reconstruction for structural consistency
`convert`  Convert morphology to compliant SWC format
`find`     Locate single nodes in the reconstruction
`measure`  Calculate morphometric features
`modify`   Manipulate morphology reconstruction
`repair`   Correct reconstruction errors
`view`     Show morphology structure
=========  =========================================================

For the detailed description of the commands and options, see 
:ref:`cli:Command-line interface`.

.. toctree::
   :hidden:

   introduction
   installation
   examples
   cli
   api

