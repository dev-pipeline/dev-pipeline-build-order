build-order
===========

Synopsis
--------
::

    dev-pipeline build-order [-h] [--method METHOD] [--list-methods]
                             [targets [targets ...]]


Description
-----------
Output a valid order to satisify the dependencies of a set of targets. The
same order is *not* guaranteed between every run, but the order will satisfy
target dependencies.


Options
-------
  -h, --help       show this help message and exit
  --method METHOD  The method used to display build order. (default: list)
  --list-methods   List the available methods instead of printing dependency
                   information. (default: False)


Available Methods
~~~~~~~~~~~~~~~~~
The tool ships with the following methods:

* :code:`dot` - *Deprecated*.  Same output as :code:`graph`.
* :code:`graph` - Output a dependency graph using dot_ syntax.  If the project
  contains a circular dependency, all components caught in the circular
  dependency will be colored red.
* :code:`layers` - Similar to :code:`graph`, but group components in a manner
  that looks like a layered architecture.  Components are organized in layers
  such that they can only depend on lower-numbered layers.
* :code:`list` - Output the build order using a comma-separated list.


Config Options
--------------
No extra configuration options.


.. _dot: https://www.graphviz.org/
