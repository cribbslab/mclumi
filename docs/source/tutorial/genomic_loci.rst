Multiple genomic loci
=====================

Different from the case used for a single genomic locus, this module allows users to deduplicate PCR artifacts/UMIs based on a set of genomic position annotations on a large scale. The usage is described below. As an example, you can download a clip of ChIP-seq data used also in UMI-tools. The dataset contains 1,175,027 reads with 20,683 raw unique UMI sequences and 12,047 genomic positions tagged by running the UMI-tools ``get_bundles`` method that is also adopted by Mclumi.

Downloading data
----------------

::

   wget https://github.com/cribbslab/mclumi/releases/download/v0.0.1/example_bundle.bam

1. CLI
------

::

   mclumi dedup_pos -m mcl -pt PO -ed 1 -infv 1.6 -expv 2 -ibam ./example_bundle.bam -obam ./basic/dedup.bam

2. Python inline
----------------

::

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
