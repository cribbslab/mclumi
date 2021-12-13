scRNA-seq
=========

``dedup_sc`` is designed for deduplicating PCR artifacts in single-cell
sequencing data.

1. CLI
------

::

   mclumi dedup_sc -m directional -gt XT -gist XS -ed 1 -ibam ./hgmm_100_STAR_FC_sorted.bam -obam ./dedup.bam

We walk you through an example input file used in UMI-tools, which can be downloaded via either https://github.com/cribbslab/mclumi/releases/download/sc_ex_hgmm_100fastq/hgmm_100_R2_extracted.fastq.gz or http://cf.10xgenomics.com/samples/cell-exp/1.3.0/hgmm_100/hgmm_100_fastqs.tar for raw reads. ``hgmm_100_STAR_FC_sorted.bam`` is a processed bam file with each read name attaching a barcode using the UMI-tools ``whitelist`` module and a UMI. Alternatively, you can also skip over to by downloading a processed bam file https://github.com/cribbslab/mclumi/releases/download/sc_ex_hgmm_100/hgmm_100_STAR_FC_sorted.bam. The single-cell dataset was derived from 10X Genomics (http://cf.10xgenomics.com/samples/cell-exp/1.3.0/hgmm_100/hgmm_100_fastqs.tar). It contains 3,553,230 raw reads. The 100 barcodes were generated using UMI-tools ``whitelist``.

1). Downloading scRNA-seq data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   https://github.com/cribbslab/mclumi/releases/download/sc_ex_hgmm_100/hgmm_100_STAR_FC_sorted.bam

2). Mapping reads
~~~~~~~~~~~~~~~~~

-  mapping tool installation

::

   wget https://github.com/alexdobin/STAR/archive/2.7.9a.tar.gz
   tar -xzf 2.7.9a.tar.gz
   cd STAR-2.7.9a
   cd STAR/source
   make STAR

   # https://github.com/alexdobin/STAR

or simply via conda

::

   conda install -c bioconda star

-  building the index of reference genome To build the index of genome
   for STAR, you should download a reference genome first. Taking a
   human genome as an example.

::

   wget ftp://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/annotation/GRCh38_latest/refseq_identifiers/GRCh38_latest_genomic.fna.gz

   wget ftp://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/annotation/GRCh38_latest/refseq_identifiers/GRCh38_latest_genomic.gff.gz

   zcat GRCh38_latest_genomic.fna.gz > GRCh38_latest_genomic.fna
   zcat GRCh38_latest_genomic.gff.gz > GRCh38_latest_genomic.gff

   STAR --runThreadN 20 --runMode genomeGenerate --genomeDir grch38_gd --genomeFastaFiles GRCh38_latest_genomic.fna --sjdbGTFfile GRCh38_latest_genomic.gff --sjdbGTFtagExonParentTranscript Parent

-  mapping

::

   STAR --runThreadN 10 --genomeDir grch38_gd/ --readFilesIn hgmm_100_R2_extracted.fastq.gz --readFilesCommand zcat --outFilterMultimapNmax 1 --outSAMtype BAM SortedByCoordinate

After mapping STAR (v2.7.9a, Dobin et al., 2012) mapping on GRCh38, 588,963 reads are left.

3). Genome annotation
~~~~~~~~~~~~~~~~~~~~~

Genes that reads belong to are annotated using featureCounts (v2.0.1, Liao et al., 2014).

::

   featureCounts -g ID -a GRCh38_latest_genomic.gff -o gene-assigned -R BAM Aligned.sortedByCoord.out.bam -T 4

   # sort index
   samtools sort Aligned.sortedByCoord.out.bam -o assigned_sorted.bam

   # rename 
   mv assigned_sorted.bam hgmm_100_STAR_FC_sorted.bam

4). Generating gene-by-cell count matrix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   mclumi dedup_sc -m directional -gt XT -gist XS -ed 1 -ibam ./hgmm_100_STAR_FC_sorted.bam -obam ./dedup.bam

``dedup.bam`` is the final results after UMI deduplication. Each read in the deduplicated file is selected as a representative from its network-based graph with the highest UMI count before deduplication. The final results look like this.

+--------------------------+-------+---+------+-----------+-----------+
| type                     | {     | a | uniq | d         | d         |
|                          | metho | v | _umi | edup_uniq | edup_read |
|                          | d}_um | e | _len | _diff_pos | _diff_pos |
|                          | i_len | _ |      |           |           |
|                          |       | e |      |           |           |
|                          |       | d |      |           |           |
|                          |       | s |      |           |           |
+==========================+=======+===+======+===========+===========+
| (‘AAAGATGAGAAACGAG’,     | 6     | 8 | 6    | 0         | 0         |
| ‘exon-NM_000099.4-3’)    |       | . |      |           |           |
|                          |       | 0 |      |           |           |
+--------------------------+-------+---+------+-----------+-----------+
| (‘AAAGATGAGAAACGAG’,     | 14    | 8 | 14   | 0         | 0         |
| ‘exon-NM_000100.4-3’)    |       | . |      |           |           |
|                          |       | 0 |      |           |           |
+--------------------------+-------+---+------+-----------+-----------+
| (‘AAAGATGAGAAACGAG’,     | 3     | 8 | 3    | 0         | 0         |
| ‘exon-NM_000101.4-6’)    |       | . |      |           |           |
|                          |       | 0 |      |           |           |
+--------------------------+-------+---+------+-----------+-----------+
| …                        | …     | … | …    | …         | …         |
+--------------------------+-------+---+------+-----------+-----------+

The second column presents dedup UMI counts (corresponding to the number of DNA molecules/transcripts) at given gene-by-cell types. Please look at `here <https://>`__ detailed explanations of the data format.

2. Python inline
----------------

The Mclumi toolkit can internally run by class ``dedupSC()`` by importing it from module ``mclumi.deduplicate.monomer``. Before running this module internally, you should also obtain a ``bam`` file first, which is completely the same as above.

::

   from mclumi.deduplicate.monomer.DedupSC import dedupSC

   umikit = dedupSC(
       mode='internal',

       # method='unique',
       method='cluster',
       # method='adjacency',
       # method='directional',
       # method='mcl',
       # method='mcl_val',
       # method='mcl_ed',

       bam_fpn='example/data/assigned_sorted.bam',
       gene_assigned_tag='XT',
       gene_is_assigned_tag='XS',
       mcl_fold_thres=1.5,
       inflat_val=1.6,
       exp_val=2,
       iter_num=100,
       verbose=True,
       ed_thres=6,
       is_sv=False,
       sv_fpn='example/data/sc/' + '' + 'assigned_sorted_dedup.bam',
   )
