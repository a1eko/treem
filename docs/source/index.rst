
treem - Neuron Morphology Processing Tool
=========================================


.. rubric:: Module ``treem``

The ``treem`` module (pronounced “trim”) provides data structures and
command-line tools for accessing and manipulating digital
reconstructions of neuronal morphology in the Stockley-Wheal-Cannon
(SWC) format.

.. rubric:: Main classes

Access to morphological data from the source code is provided through
the classes ``Tree``, ``Node``, ``Morph``, and ``SWC``:

=========  =========================================================
``Tree``   Recursive tree data structure
``Node``   Morphology data storage
``Morph``  Neuron morphology representation
``SWC``    Definitions of the data format
=========  =========================================================

For the complete list of available functions, see :ref:`api:API
reference`.


.. rubric:: Commands

Common operations with SWC files can be performed using the ``swc``
command-line tool::

    swc <command> [options] file

Alternatively::

    swc <command> file [file ...] [options] 

List of ``swc`` commands:

=========  =========================================================
`check`    Tests the morphology reconstruction for structural consistency
`convert`  Converts morphology data to a compliant SWC format
`find`     Locates individual nodes in the reconstruction
`measure`  Calculates morphometric features
`modify`   Modifies morphology reconstruction
`render`   Displays a 3D model of the reconstruction
`repair`   Corrects reconstruction errors
`view`     Displays the morphology structure
=========  =========================================================

For detailed description of all commands and their options, see the
:ref:`cli:Command-line interface`.

.. toctree::
   :hidden:

   introduction
   installation
   examples
   cli
   api
