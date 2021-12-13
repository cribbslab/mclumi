.. mclumi documentation master file, created by
   sphinx-quickstart on Fri Oct 22 01:46:02 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Tutorials
=========
In the tutorials, we will go through a few number of using Mclumi. For data preprocessing, users should check out the trim section first before mapping. After trimming, mapping, and annotating reads, Mclumi performs UMI deduplication -at the four application scenarios- in regard to a single genomic locus, multiple genomic loci, genes, and cell-by-gene types. Among the scenarios, we specifically detail how to step-by-step deduplicate UMIs from scRNA-seq sequencing data. Each scenario, Mclumi provides both of Python inline and command line interfaces for use.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   trim
   a_single_genomic_locus
   bulkRNAseq
   genomic_loci
   scRNAseq

