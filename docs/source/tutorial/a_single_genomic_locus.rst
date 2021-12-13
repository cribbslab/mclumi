A single genomic locus
======================

The Mclumi ``dedup_basic`` module allows users to work out a
deduplicated molecules at a given genomic locus. This module can be seen
as the most basic unit of deduplicating other RNA-seq reads and it
simply gives a line of summarized statistics.

1. CLI
------

::

   mclumi dedup_basic -m mcl -ed 1 -infv 1.6 -expv 2 -ibam ./example_bundle.bam -obam ./dedup.bam

2. Python inline
----------------

.. code:: python=

   from mclumi.deduplicate.monomer.DedupBasic import dedupBasic

   umikit = dedupBasic(
           mode='internal',

           # method='unique',
           # method='cluster',
           # method='adjacency',
           # method='directional',
           method='mcl',
           # method='mcl_val',
           # method='mcl_ed',

           bam_fpn='example/data/example_bundle.bam',
           mcl_fold_thres=1.5,
           inflat_val=1.6,
           exp_val=2,
           iter_num=100,
           verbose=True,
           ed_thres=1,
           is_sv=False,
           sv_fpn='example/data/basic/assigned_sorted_dedup.bam',
       )

.. code:: shell=

   run Mclumi internally.
   22/10/2021 20:09:44 logger: ===>reading the bam file... /home/students/j.sun/store/software/us/mcl/mclumi/example/data/example_bundle.bam
   [E::idx_find_and_load] Could not retrieve index file for '/home/students/j.sun/store/software/us/mcl/mclumi/example/data/example_bundle.bam'
   22/10/2021 20:09:44 logger: ===>reading BAM time: 0.00s
   22/10/2021 20:09:44 logger: =========>start converting bam to df...
   22/10/2021 20:09:53 logger: =========>time to df: 8.247s
   22/10/2021 20:09:53 logger: ======># of raw reads: 1175027
   22/10/2021 20:09:53 logger: ======># of reads with qualified chrs: 1175027
   22/10/2021 20:09:53 logger: ======># of unique umis: 1949
   22/10/2021 20:09:53 logger: ======># of redundant umis: 1175027
   22/10/2021 20:09:53 logger: ======>edit distance thres: 1
   22/10/2021 20:09:53 logger: ===>start building umi graphs...
   22/10/2021 20:10:35 logger: ===>time for building umi graphs: 41.11s
   22/10/2021 20:10:35 logger: ===>start deduplication by the mcl method...
   22/10/2021 20:10:41 logger: ======>finish finding deduplicated umis in 6.17s
   22/10/2021 20:10:41 logger: ======># of umis deduplicated to be 44
   22/10/2021 20:10:41 logger: ======>calculate average edit distances between umis...
   22/10/2021 20:10:41 logger: ======>finish calculating ave eds in 0.00s
   22/10/2021 20:10:41 logger: ======># of deduplicated unique umis 1905 on the basis of the unique method
   22/10/2021 20:10:41 logger: ======># of deduplicated reads 1116981 on the basis of the unique method
   5.0    1
   Name: ave_eds, dtype: int64
   22/10/2021 20:10:41 logger: ======>start writing deduplicated reads to BAM...
   22/10/2021 20:10:41 logger: ======># of the total reads left after deduplication: 44
   22/10/2021 20:10:41 logger: ======>finish writing in 0.00s
