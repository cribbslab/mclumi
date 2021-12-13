.. mclumi documentation master file, created by
   sphinx-quickstart on Fri Oct 22 01:46:02 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Mclumi Homepage
===============

|image0| |image1| |image2| |image3| |Documentation Status| |Downloads|

Mclumi is a toolkit developed by Markov clustering (MCL) network-based
algorithms for precisely localizing unique UMIs and thus removing PCR
duplicates. Mclumi is a Python implementation and interaction between
methods and modules in it is through object-oriented programming (OOP).
It provides a collection of modules, including 4 main modules,
``dedup_basic``, ``dedup_pos``, ``dedup_gene``, and
``dedup_sc`` and 1 addition module ``trim``. For UMI
deduplication, each main module includes 7 algorithms ``unique``,
cluster, ``adjacency``, ``directional``, ``mcl``,
``mcl_ed``, and ``mcl_val`` that take as input a bam file and
output a deduplicated bam file and another 2 summary files. Every module
in Mclumi can be run internally (Python inline) or externally (CLI).

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quick_start_guide
   tutorial/index
   format/index
   modules

Features
--------

-  Clustering based on edit distance
-  Flexible and extendable

   -  Dispering: increase the number of subcomponents
   -  Shrinking: decrease the number of subcomponents
   -  Parameterized control

-  More accurate for quantification esimate of molecules

Changelogs
----------

[v0.0.4] Adding documentation to Mclumi.

[v0.0.3] A stable version of Mclumi.

[v0.0.2] Codes linked to readthedocs.

[v0.0.2] A test version of Mclumi.

Contributors
------------

`Jianfeng Sun <https://www.ndorms.ox.ac.uk/team/jianfeng-sun>`__ `Adam
Cribbs <https://www.ndorms.ox.ac.uk/team/adam-cribbs>`__

.. |image0| image:: https://img.shields.io/badge/Mclumi-executable-519dd9.svg
.. |image1| image:: https://img.shields.io/badge/last_released-Oct._2021-green.svg
.. |image2| image:: https://img.shields.io/github/stars/cribbslab/mclumi?logo=GitHub&color=blue
.. |image3| image:: https://img.shields.io/pypi/v/mclumix?logo=PyPI
.. |Documentation Status| image:: https://readthedocs.org/projects/mclumi/badge/?version=latest
   :target: https://mclumi.readthedocs.io/en/latest/?badge=latest
.. |Downloads| image:: https://pepy.tech/badge/mclumi
   :target: https://pepy.tech/project/mclumi


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
