Quick start guide
=================

Overview
--------

We set up a quick start guide to walk you through an example to use Mclumi. Mclumi provides 7 methods for UMI deduplication, that is, ``unique``, ``cluster``, ``adjacency``, ``directional``, ``mcl``, ``mcl_ed``, and ``mcl_val``, and 4 modules for handling 4 types of application scenarios, that is, a single genomic locus, multiple genomic loci, genes, and cell-by-gene types.

Documentation
-------------

The API documentation of Mclumi is available at Readthedocs
https://mclumi.readthedocs.io/en/latest/.

System Requirement
------------------

Linux or Mac

Installation
------------

-  PyPI https://pypi.org/project/mclumix/

::

   pip install --upgrade mclumix

Usage
-----

Command-Line Interface (CLI)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Overview

::

   usage: mclumi [-h] [--read_structure read_structure] [--lens lens]
                 [--input input] [--output output] [--method method]
                 [--input_bam input_bam] [--edit_dist edit dist]
                 [--inflation_value inflation_value]
                 [--expansion_value expansion_value]
                 [--iteration_number iteration_number]
                 [--mcl_fold_thres mcl_fold_thres] [--is_sv is_sv]
                 [--output_bam output_bam] [--verbose verbose]
                 [--pos_tag pos_tag] [--gene_assigned_tag gene_assigned_tag]
                 [--gene_is_assigned_tag gene_is_assigned_tag]
                 tool

   Welcome to the mclumi toolkit

   positional arguments:
     tool                  trim, dedup_basic, dedup_pos, dedup_gene, dedup_sc

   optional arguments:
     -h, --help            show this help message and exit
     --read_structure read_structure, -rs read_structure
                           str - the read structure with elements in conjunction
                           with +, e.g., primer_1+umi_1+seq_1+umi_2+primer_2
     --lens lens, -l lens  str - lengths of all sub-structures separated by +,
                           e.g., 20+10+40+10+20 if the read structure is
                           primer_1+umi_1+seq_1+umi_2+primer_2
     --input input, -i input
                           str - input a fastq file in gz format for trimming
                           UMIs
     --output output, -o output
                           str - output a UMI-trimmed fastq file in gz format.
     --method method, -m method
                           str - a dedup method: unique | cluster | adjacency |
                           directional | mcl | mcl_ed | mcl_val
     --input_bam input_bam, -ibam input_bam
                           str - input a bam file curated by requirements of
                           different dedup modules: dedup_basic, dedup_pos,
                           dedup_gene, dedup_sc
     --edit_dist edit dist, -ed edit dist
                           int - an edit distance used for building graphs at a
                           range of [1, l) where l is the length of a UMI
     --inflation_value inflation_value, -infv inflation_value
                           float - an inflation value for MCL, 2.0 by default
     --expansion_value expansion_value, -expv expansion_value
                           int - an expansion value for MCL at a range of (1,
                           +inf), 2 by default
     --iteration_number iteration_number, -itern iteration_number
                           int - iteration number for MCL at a range of (1,
                           +inf), 100 by default
     --mcl_fold_thres mcl_fold_thres, -fthres mcl_fold_thres
                           float - a fold threshold for MCL at a range of (1, l)
                           where l is the length of a UMI.
     --is_sv is_sv, -issv is_sv
                           bool - to make sure if the deduplicated reads writes
                           to a bam file (True by default or False)
     --output_bam output_bam, -obam output_bam
                           str - output UMI-deduplicated summary statistics to a
                           txt file.
     --verbose verbose, -vb verbose
                           bool - to enable if output logs are on console (True
                           by default or False)
     --pos_tag pos_tag, -pt pos_tag
                           str - to enable deduplication on the position tags (PO
                           recommended when your bam is tagged)
     --gene_assigned_tag gene_assigned_tag, -gt gene_assigned_tag
                           str - to enable deduplication on the gene tag (XT
                           recommended)
     --gene_is_assigned_tag gene_is_assigned_tag, -gist gene_is_assigned_tag
                           str - to check if reads are assigned the gene tag (XS
                           recommended)

Deduplication according to genomic positions
--------------------------------------------

``dedup_pos`` is taken as an example. It allows users to deduplicate PCR artifacts/UMIs based on a set of genomic position annotations on a large scale. In the quick start guide, we omitted some data preprocessing procedures and start from introduing a dataset (a clip of ChIP-seq data used also in UMI-tools) contains 1,175,027 reads with 20,683 raw unique UMI sequences and 12,047 genomic positions tagged by running the UMI-tools ``get_bundles`` method that is also adopted by Mclumi in which it can be accessed by the  ``mclumi.align.BundlePos`` module.

Downloading data
----------------

::

   wget https://github.com/cribbslab/mclumi/releases/download/v0.0.1/example_bundle.bam

Running Mclumi
--------------

::

   # CLI
   mclumi dedup_pos -m mcl -pt PO -ed 1 -infv 1.6 -expv 2 -ibam ./example_bundle.bam -obam ./basic/dedup.bam

   # or Python inline
   from mclumi.deduplicate.monomer.DedupPos import dedupPos

   umikit = dedupPos(
       mode='internal',

       # method='unique',
       method='cluster',
       # method='adjacency',
       # method='directional',
       # method='mcl',
       # method='mcl_val',
       # method='mcl_ed',

       bam_fpn='example/data/example_bundle.bam',
       pos_tag='PO',
       mcl_fold_thres=1.5,
       inflat_val=1.6,
       exp_val=2,
       iter_num=100,
       verbose=True,
       ed_thres=1,
       is_sv=False,
       sv_fpn='example/data/pos/assigned_sorted_dedup.bam',
   )

Result interpretation
---------------------

The Mcluim dedup_pos module returns two files as follows.

1. ``{method}_ave_ed_pos_bin.txt``
2. ``{method}_dedup_sum.txt``

where {method} represents the ``unique``, ``adjacency``, ``directional``, ``mcl``, ``mcl_val``, or ``mcl_ed`` method, correspondingly. ``{method}_ave_ed_pos_bin.txt`` mainly summerizes the total number of genomic positions with respect to their average edit distances (Figures 1 and 2). Further explanations can be found on output_format_.

.. _output_format: https://mclumi.readthedocs.io/en/latest/format/output_format.html

All methods in UMI-tools are reconstructed in Mcluim by implementing the ``cluster`` and ``adjacency`` methods based on the breadth first search (BFS) algorithm and the directional method based on the depth first search (DFS) algorithm. After then, in order to test whether these methods are implemented correctly, the two software packages were performed on the above dataset, and the results of deduplication show that the directional method (the rest two (not shown) are the same as well) from either software performs identically. Other methods are shown in Figure 2.

|image0| Figure 1. Comparison of performance of the UMI-tools directional method and the Mclumi directional method.

|image1| Figure 2. Profile of average edit distances of all methods.

Contact
-------

Homepage: https://www.ndorms.ox.ac.uk/team/adam-cribbs

.. |image0| image:: https://github.com/cribbslab/mclumi/blob/main/imgs/ave_eds.jpg?raw=true
.. |image1| image:: https://github.com/cribbslab/mclumi/blob/main/imgs/all_ave_eds.jpg?raw=true
