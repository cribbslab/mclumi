Input format
============

BAM file
--------

Mclumi receives a ``bam`` file as input by default after using a
trimmed ``*.fastq.gz`` file with each read umi attached to the read
name. In single cell analysis, barcodes will be attached to the read
name prior to their UMIs. The ``*.fastq.gz`` can be mapped on a
reference genome as a ``bam`` file using a mapping tool, such as
`HISAT2 <http://daehwankimlab.github.io/hisat2/>`__ or
`STAR <https://github.com/alexdobin/STAR>`__. For simulation purposes,
the bam file can be generated using another pipeline called simReadFlow,
which uses a ``fastq.gz`` file as input directly and outputs a
``bam`` file because simReadFlow will control the format of
simulated ``fastq.gz`` files to be recognized by trimming module.

UMI-tools preprocessed BAM file
-------------------------------

Besides, we noticed that a well-curated module for preprocessing a BAM
file is embedded in UMI-tools. To enable use of this UMI-tools module in
Mclumi, you can import a module ``BundlePos`` with its class object
``bundlePos`` to deal with this issue. All qualified reads will be
accessible to section ``tags`` ``PO='pos'`` in the bundle
``bam`` file. Unqualified reads are filtered by UMI-tools modules,
due to factors such as poorly recognized contigs.

::

   from mclumi.align.BundlePos import bundlePos
   in_fpn = to('your_working_path/example.bam')
   out_fpn = to('your_working_path/example_bundle.bam')
   bundlePos.convert(options=options, in_fpn=in_fpn, out_fpn=out_fpn)
