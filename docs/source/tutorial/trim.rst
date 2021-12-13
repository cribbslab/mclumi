Trim
====

The Mclumi ``Trim`` module allows users to trim UMI(s) and/or barcode(s) of any length as well as other components (e.g., primer) from a complex read structure, which is much more flexible than other UMI tools. For instance, it can be used for trimming from reads sequenced by template bulk-RNA-seq and scRNA-seq and so on. The module works based on a clear defined structure of a read. Therefore, the module needs the read length to be indentical for all as well as UMI-tools does. In python inline mode, a set of parameters need to be specified in json format for the composition/structure of your input reads. For example, an input read consists of a barcode first, a umi then, and a read finally. Details of an exmaple of reads by template switching oligos (TSO) are given below.

Python inline
-------------

.. code:: jsonld

   {
       # umis
       'umi_1': {
           'len': 12,
       },
       'umi_2': {
           'len': 12,
       },
       # ...,

       # reads
       'seq_1': {
           'len': 30,
       },
       'seq_2': {
           'len': 30,
       },
       # ...,

       # other components, e.g.,
       'bc_1': {
           'len': 20,
       },
       # ...,
       
       'read_struct': 'bc_1+umi_1+seq_1+umi_2',
       'fastq': {
           'fpn': 'xxx.fastq.gz',
           'trimmed_fpn': 'xxx_trim.fastq.gz',
       },
   }

.. code:: jsonld

   from mclumi.trim.Fixed import fixed
   p = fixed(
       mode='internal',
       params=params,
   )
   p.call()

As an example, we take a simulated fastq file of small size, which can be download via `pcr_1.fastq.gz <https://github.com/cribbslab/mclumi/releases/download/exfastq/pcr_1.fastq.gz>`__.

If you tend to run Mclumi in inline mode, the parameter of ``mode`` should be specified as ``internal``. This will tell Mclumi to run the Trim module inline. After running starts, the module pops out prompts like this

.. code:: shell

   22/10/2021 20:03:28 logger: run Mclumi internally.
   22/10/2021 20:03:28 logger: Your params for trimming UMIs are: 
   {'umi_1': {'len': 12}, 'umi_2': {'len': 10}, 'umi_3': {'len': 12}, 'primer_1': {'len': 20}, 'primer_2': {'len': 20}, 'seq_1': {'len': 6}, 'seq_2': {'len': 8}, 'read_struct': 'primer_1+umi_1+seq_1+umi_2+primer_2', 'fastq': {'fpn': 'pcr_1.fastq.gz', 'trimmed_fpn': 'pcr_1_trim.fastq.gz'}}
   22/10/2021 20:03:28 logger: ===>reading from fastq...
   22/10/2021 20:03:28 logger: ===>umi structure: primer_1+umi_1+seq_1+umi_2+primer_2
   22/10/2021 20:03:28 logger: ===>umi positions in the read structure: 1, 3
   22/10/2021 20:03:28 logger: ===>seq positions in the read structure: 2
   22/10/2021 20:03:28 logger: ======>finding the starting positions of all UMIs...
   22/10/2021 20:03:28 logger: =========>umi_1 starting position: 20
   22/10/2021 20:03:28 logger: =========>umi_2 starting position: 38
   22/10/2021 20:03:28 logger: ======>finding the starting positions of all genomic sequence...
   22/10/2021 20:03:28 logger: =========>seq_1 starting position: 32
   22/10/2021 20:03:28 logger: ===>umi_1 has been taken out
   22/10/2021 20:03:28 logger: ===>umi_2 has been taken out
   22/10/2021 20:03:28 logger: ===>seq_1 has been taken out
   22/10/2021 20:03:28 logger: ===>start saving in gz format...
   22/10/2021 20:03:28 logger: ===>trimmed UMIs have been saved in gz format.

CLI
---

If you tend to run Mclumi in CLI, only quite a few differences should be made. ``-l`` the lengths of different components should also be concatenated by +.

::

   mclumi trim -i ./pcr_1.fastq.gz -o ./pcr_trimmed.fastq.gz -rs primer_1+umi_1+seq_1+umi_2+primer_2 -l 20+10+40+10+20
