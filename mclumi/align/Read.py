__version__ = "v1.0"
__copyright__ = "Copyright 2021"
__license__ = "MIT"
__lab__ = "Adam Cribbs lab"

import time
import pysam
import pandas as pd
from mclumi.util.Console import console


class read(object):

    def __init__(self, bam_fpn, verbose=False):
        """
        # pos_last = 0
        # chr_last = 0
        # if read.pos <= (pos_last + 1000) and read.reference_id == chr_last:
        # print(read.pos, pos_last, read.reference_id)
        # pos_last = read.pos
        # chr_last = read.reference_id
        Parameters
        ----------
        bam_fpn
        verbose
        """
        self.console = console()
        self.console.verbose = verbose
        self.console.print('===>reading the bam file... {}'.format(bam_fpn))
        read_bam_stime = time.time()
        self.pysam_bam = pysam.AlignmentFile(bam_fpn, "rb")
        self.console.print('===>reading BAM time: {:.2f}s'.format(time.time() - read_bam_stime))

    def bycol(self, col='sname'):
        """

        Parameters
        ----------
        col

        Returns
        -------

        """
        t = []
        if col == 'sname':
            for id, read in enumerate(self.pysam_bam):
                # print(read)
                # print(read.get_tags())
                if read.reference_id != -1:
                    tt = read.query_name
                else:
                    continue
                t.append(tt)
            return pd.DataFrame(t)

    def todf(self, tags=[]):
        """

        Notes
        -----
        11 columns from alignments deciphered by Pysam
            # read.query_name
            # read.flag
            # read.reference_id
            # read.reference_start
            # read.mapping_quality
            # read.cigar
            # read.query_sequence
            # read.next_reference_id
            # read.next_reference_start
            # read.template_length
            # read.query_qualities

        See Also
        --------
        https://pysam.readthedocs.io/en/latest/usage.html#creating-bam-cram-sam-files-from-scratch
        https://pysam.readthedocs.io/_/downloads/en/v0.12.0/pdf/

        Parameters
        ----------
        tags

        Returns
        -------

        """
        l = []
        self.console.print('=========>start converting bam to df...')
        import time
        stime = time.time()
        for id, read in enumerate(self.pysam_bam):
            # print(read)
            read_tags = read.get_tags()
            # print(read_tags)
            rt_dict = {k: v for k, v in read_tags}
            rt_keys = [*rt_dict.keys()]
            # print(rt_keys)
            tag_keys = [rt_dict[k] if k in rt_keys else 'None' for k in tags]
            # print(tag_keys)
            vignette = [
                id,
                read.query_name,
                read.flag,
                read.reference_id,
                read.pos,
                read.mapping_quality,
                read.cigar,
                read.query_sequence,
                read.next_reference_id,
                read.next_reference_start,
                read.template_length,
                read.query_qualities,
                read,
            ] + tag_keys
            l.append(vignette)
        df = pd.DataFrame(
            l,
            columns=[
                'id',
                'query_name',
                'flag',
                'reference_id',
                'pos',
                'mapping_quality',
                'cigar',
                'query_sequence',
                'next_reference_id',
                'next_reference_start',
                'template_length',
                'query_qualities',
                'read',
            ] + tags,
        )
        if 'XS' in tags and 'XT' in tags:
            stat_XT = df['XS'].value_counts()
            if 'None' in stat_XT.keys():
                if stat_XT['None'] == df.shape[0]:
                    df['XS'] = df['XT'].apply(lambda x: 'Assigned' if x != 'None' else 'Unassigned')
        # print(df['XA'].loc[df['reference_id'] != -1].shape)
        # print(df['MD'].loc[df['MD'] != 'None'].shape)
        # print(df['NM'].loc[df['NM'] != 'None'].shape)
        # print(df['XS'].loc[df['XS'] != 'None'].shape)
        # print(df['XT'].loc[df['XT'] != 'None'].shape)
        self.console.print('=========>time to df: {:.3f}s'.format(time.time() - stime))
        return df
    
    def todf11(self, ):
        """
        Notes
        -----
        11 columns from alignments deciphered by Pysam
            # read.query_name
            # read.flag
            # read.reference_id
            # read.reference_start
            # read.mapping_quality
            # read.cigar
            # read.query_sequence
            # read.next_reference_id
            # read.next_reference_start
            # read.template_length
            # read.query_qualities

        See Also
        --------
        https://pysam.readthedocs.io/en/latest/usage.html#creating-bam-cram-sam-files-from-scratch
        https://pysam.readthedocs.io/_/downloads/en/v0.12.0/pdf/

        Returns
        -------

        """
        l = []
        self.console.print('=========>start converting bam to df...')
        stime = time.time()
        for id, read in enumerate(self.pysam_bam):
            l.append([
                id,
                read.query_name,
                read.flag,
                read.reference_id,
                read.reference_start,
                read.mapping_quality,
                read.cigar,
                read.query_sequence,
                read.next_reference_id,
                read.next_reference_start,
                read.template_length,
                read.query_qualities,
            ])
        df = pd.DataFrame.from_dict(
            l,
            columns=[
                'id',
                'query_name',
                'flag',
                'reference_id',
                'reference_start',
                'mapping_quality',
                'cigar',
                'query_sequence',
                'next_reference_id',
                'next_reference_start',
                'template_length',
                'query_qualities',
            ],
        )
        self.console.print('=========>time to df: {:.3f}s'.format(time.time() - stime))
        return df

    def todf11_depr(self, ):
        """
        Note
        ----
        Deprecated.

        Returns
        -------
        Dataframe of a bam file

        """
        l = []
        self.console.print('=========>start converting bam to df')
        import time
        stime = time.time()
        for id, read in enumerate(self.pysam_bam):
            read_piece = {
                'id': id,
                'query_name': read.query_name,
                'flag': read.flag,
                'reference_id': read.reference_id,
                'reference_start': read.reference_start,
                'mapping_quality': read.mapping_quality,
                'cigar': read.cigar,
                'query_sequence': read.query_sequence,
                'next_reference_id': read.next_reference_id,
                'next_reference_start': read.next_reference_start,
                'template_length': read.template_length,
                'query_qualities': read.query_qualities,
            }
            l.append(read_piece)
        df = pd.DataFrame.from_dict(l)
        self.console.print('=========>time to df: {:.3f}s'.format(time.time() - stime))
        return df


if __name__ == "__main__":
    from mclumi.Path import to

    umikit = read(
        # bam_fpn=to('example/data/example.bam'),
        # bam_fpn=to('example/data/example_buddle.bam'),
        # to('example/data/assigned_sorted.bam')
        # to('example/data/assigned_sorted_dedup.bam')
        # bam_fpn=to('example/data/deduplicated.bam'),
        # bam_fpn=to('example/data/RM82CLK1_S3_featurecounts_gene_sorted.bam'),
        bam_fpn=to('example/data/RM82_CLK1_DMSO_2_XT.bam'),
    )

    # df = umikit.todf(tags=['PO'])
    # df = umikit.todf(tags=['XS', 'XT'])
    # print(df)
    #
    # df = df.loc[df['XS'] == 'Assigned']
    # print(df)
    df = umikit.todf(tags=['XT', 'XS'])
    print(df)
