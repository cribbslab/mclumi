Output format
=============

Mclumi provides three output files after running each of the ``dedup_basic``, ``dedup_pos``, ``dedup_gene``, and ``dedup_sc`` modules, with the following names.

1. ``{method}_ave_ed_pos_bin.txt``
2. ``{method}_dedup_sum.txt``
3. ``{name}_dedup.bam``

Please note that ``{method}`` above refers to ``{uniq}``, ``{cc}``, ``{adj}``, ``{direc}``, ``{mcl}``, ``{mcl_val}``, or ``{mcl_ed}`` standing for the ``unique``, ``adjacency``, ``directional``, ``mcl``, ``mcl_val``, or ``mcl_ed`` method, correspondingly. ``{name}`` can be designated by users. Result format is spelt out below.

1. Single genomic position/gene/gene-by-cell result format
----------------------------------------------------------

After running module ``dedup_basic``, the results will be stored in a ``{method}_ave_ed_pos_bin.txt`` file and a ``{method}_dedup_sum.txt`` file indicating deduplicated UMI counts across all reads in a given bam file.

2. Genomic position result format
---------------------------------

``{method}_ave_ed_pos_bin.txt``

Data at the third row is interpreted as: the number of genomic positions observed with an average edit distance 3 between UMIs is 4.

============= ======
edit distance number
============= ======
-1.0          3652
2.0           1
3.0           4
…             …
============= ======

-  the **1st** column: average edit distance between UMIs at genomic
   positions
-  the **2nd** column: number of gene-by-cell types observed with those
   average edit distance, respectively
-  -1.0 represents that only one unique umi seen at a single genomic
   position; in total there are 3652 genomic positions seen with one
   unique umi.

``{method}_dedup_sum.txt``

+------------+--------+-----+---------+---------------+---------------+
| No.        | {met   | a   | uniq_   | dedup_        | dedup_        |
|            | hod}_u | ve_ | umi_len | uniq_diff_pos | read_diff_pos |
|            | mi_len | eds |         |               |               |
+============+========+=====+=========+===============+===============+
| 0          | 4      | 4.0 | 4       | 0             | 0             |
+------------+--------+-----+---------+---------------+---------------+
| 1          | 2      | 5.0 | 2       | 0             | 0             |
+------------+--------+-----+---------+---------------+---------------+
| 2          | 7      | 4.0 | 9       | 2             | 2             |
+------------+--------+-----+---------+---------------+---------------+
| …          | …      | …   | …       | …             | …             |
+------------+--------+-----+---------+---------------+---------------+

-  the **1st** column: genomic positions of interest
-  the **2nd** column: deduplicated UMI counts (corresponding to the
   number of DNA molecules/transcripts) at genomic positions
-  the **3rd** column: average edit distances between UMIs at given
   genomic positions
-  the **4th** column: unique UMI counts at given genomic positions
-  the **5th** column: difference in dedup UMI counts and original
   unique UMI counts
-  the **6th** column: difference in the number of dedup reads and
   original reads

3. bulk RNA-seq result format
-----------------------------

``{method}_ave_ed_pos_bin.txt``

Spelling out results

Data at the third row is interpreted as: the number of gene types observed with an average edit distance 3 between UMIs is 4.

============= ======
edit distance number
============= ======
-1.0          3652
2.0           1
3.0           4
…             …
============= ======

-  the **1st** column: average edit distance between UMIs at gene types
-  the **2nd** column: number of gene types observed with those average
   edit distances, respectively
-  -1.0 represents that only one unique umi seen at a single gene type;
   in total there are 3652 genomic positions seen with one unique umi.

``{method}_dedup_sum.txt``

+------------+--------+-----+---------+---------------+---------------+
| type       | {met   | ave_eds   | uniq_   | dedup_        | dedup_        |
|            | hod}_u |  | umi_len | uniq_diff_pos | read_diff_pos |
|            | mi_len |  |         |               |               |
+============+========+=====+=========+===============+===============+
| ENSG0     | 5      | 1   | 5       | 0             | 0             |
| 0000000003 |        | 1.0 |         |               |               |
+------------+--------+-----+---------+---------------+---------------+
| ENSG0      | 7      | 1   | 8       | 1             | 1             |
| 0000000419 |        | 2.0 |         |               |               |
+------------+--------+-----+---------+---------------+---------------+
| ENSG0      | 2      | 1   | 2       | 0             | 0             |
| 0000000457 |        | 1.0 |         |               |               |
+------------+--------+-----+---------+---------------+---------------+
| …          | …      | …   | …       | …             | …             |
+------------+--------+-----+---------+---------------+---------------+

-  the **1st** column: gene types
-  the **2nd** column: deduplicated UMI counts (corresponding to the
   number of DNA molecules/transcripts) at a given gene type
-  the **3rd** column: average edit distances between UMIs at given gene
   types
-  the **4th** column: unique UMI counts at given gene types
-  the **5th** column: difference in dedup UMI counts and original
   unique UMI counts
-  the **6th** column: difference in the number of dedup reads and
   original reads

4. scRNA-seq data format
------------------------

Data at the third row is interpreted as: the number of gene-by-cell
types observed with an average edit distance 3 between UMIs is 4.

``{method}_ave_ed_pos_bin.txt``

============= ======
edit distance number
============= ======
-1.0          3652
2.0           1
3.0           4
…             …
============= ======

-  the **1st** column: average edit distance between UMIs at
   gene-by-cell types
-  the **2nd** column: number of gene-by-cell types observed with those average edit distances, respectively

``{method}_dedup_sum.txt``

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

-  the **1st** column: gene-by-cell types
-  the **2nd** column: dedup UMI counts (corresponding to the number of
   DNA molecules/transcripts) at given gene-by-cell types
-  the **3rd** column: average edit distance between UMIs at
   gene-by-cell types
-  the **4th** column: average edit distance between UMIs at given
   gene-by-cell types
-  the **5th** column: unique UMI counts at given gene-by-cell types
-  the **6th** column: difference in dedup UMI counts and original
   unique UMI counts
-  the **7th** column: difference in the number of dedup reads and
   original reads
