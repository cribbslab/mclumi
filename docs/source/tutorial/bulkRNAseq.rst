bulk RNA-seq
============

A typical application scenario for using ``dedup_gene`` is when it is applied for bulk RNA-seq reads annotated with gene tags. But this can definitely be used for reads using other sequencing techniques. designed for deduplicating PCR artifacts in single-cell sequencing data.

Downloading data
----------------

::

   wget https://github.com/cribbslab/mclumi/releases/download/sc_ex_hgmm_100/hgmm_100_STAR_FC_sorted.bam

1. CLI
------

::

   mclumi dedup_gene -m directional -gt XT -gist XS -ed 1 -ibam ./hgmm_100_STAR_FC_sorted.bam -obam ./dedup.bam

2. Python inline
----------------

::

   from mclumi.deduplicate.monomer.DedupGene import dedupGene

   umikit = dedupGene(
       mode='internal',

       # method='unique',
       method='cluster',
       # method='adjacency',
       # method='directional',
       # method='mcl',
       # method='mcl_val',
       # method='mcl_ed',

       bam_fpn='example/data/hgmm_100_STAR_FC_sorted.bam',
       gene_assigned_tag='XT',
       gene_is_assigned_tag='XS',
       mcl_fold_thres=1.5,
       inflat_val=1.6,
       exp_val=2,
       iter_num=100,
       verbose=True,
       ed_thres=6,
       is_sv=False,
       sv_fpn='example/data/gene/assigned_sorted_dedup.bam',
   )
