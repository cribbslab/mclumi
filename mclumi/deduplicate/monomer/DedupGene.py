__version__ = "v1.0"
__copyright__ = "Copyright 2021"
__license__ = "MIT"
__lab__ = "Adam Cribbs lab"

import os
import sys
import time
import argparse
import numpy as np
import pandas as pd
from mclumi.align.Read import read as aliread
from mclumi.align.Write import write as aliwrite
from mclumi.util.Writer import writer as gwriter
from mclumi.util.Hamming import hamming
from mclumi.util.Number import number as rannum
from mclumi.util.Console import console
from mclumi.deduplicate.monomer.Build import build as umibuild
# from mclumi.deduplicate.monomer.Build_test import build as umibuild
from mclumi.deduplicate.monomer.Cluster import cluster as umimonoclust
from mclumi.deduplicate.monomer.Adjacency import adjacency as umitoolmonoadj
from mclumi.deduplicate.monomer.Directional import directional as umitoolmonodirec
from mclumi.deduplicate.monomer.MarkovClustering import markovClustering as umimonomcl
sys.setrecursionlimit(15000000)


class dedupGene():

    def __init__(self, bam_fpn, ed_thres, method, gene_assigned_tag, gene_is_assigned_tag, mode='internal', mcl_fold_thres=None, inflat_val=2.0, exp_val=2, iter_num=100, is_sv=True, sv_fpn='./dedup.bam', sv_dsum_fpn='./dedup_sum.txt', sv_aed_fpn='None', verbose=False):
        """
        Parameters
        ----------
        bam_fpn
            str - the full path of a BAM file curated by requirements of different dedup modules
        ed_thres
            int - an edit distance threshold (>1, integer)
        method
            str - a deduplication method (mcl, mcl_val, mcl_ed, cluster, unique, ajacency, directional)
        mode
            str - externally or internally run the module (external by defualt, internal)
        mcl_fold_thres
            float - a mcl fold threshold (1.5 by defualt)
        inflat_val
            float - an inflation value for generating mcl clusters (2.0 by defualt)
        exp_val
            int - an expansion value for generating mcl clusters (2 by defualt)
        iter_num
            int - number of iterations for mcl (100 by defualt)
        is_sv
            bool - is the deduplicated bam file to save (True by default or False)
        sv_fpn
            str - the deduplication file path
        verbose
            bool - print log on the console, (True by default or False)
        """
        self.rannum = rannum()
        self.gwriter = gwriter()
        self.umibuild = umibuild

        if mode == 'internal':
            self.method = method
            self.bam_fpn = bam_fpn
            self.ed_thres = ed_thres
            self.gene_assigned_tag = gene_assigned_tag
            self.gene_is_assigned_tag = gene_is_assigned_tag
            self.mcl_fold_thres = mcl_fold_thres
            self.inflat_val = inflat_val
            self.exp_val = exp_val
            self.iter_num = iter_num
            self.is_sv = is_sv
            self.sv_fpn = sv_fpn
            self.sv_dsum_fpn = sv_dsum_fpn
            self.sv_aed_fpn = sv_aed_fpn
            self.verbose = verbose
            print('run Mclumi internally.')
        else:
            self.parser = argparse.ArgumentParser(
                description='The dedupGene module'
            )
            self.parser.add_argument(
                "--method", "-m",
                metavar='method',
                dest='m',
                required=True,
                type=str,
                help='str - a dedup method: unique | cluster | adjacency | directional | mcl | mcl_ed | mcl_val',
            )
            self.parser.add_argument(
                "--input_bam", "-ibam",
                metavar='input_bam',
                dest='ibam',
                required=True,
                type=str,
                help='str - input a bam file annotated with gene information in the tag field of the bam file.',
            )
            self.parser.add_argument(
                "--edit_dist", "-ed",
                metavar='edit dist',
                dest='ed',
                default=1,
                type=int,
                help='int - an edit distance used for building graphs (int >1)',
            )
            self.parser.add_argument(
                "--inflation_value", "-infv",
                metavar='inflation_value',
                dest='infv',
                default=2.0,
                type=float,
                help='an inflation value for MCL',
            )
            self.parser.add_argument(
                "--expansion_value", "-expv",
                metavar='expansion_value',
                dest='expv',
                default=2,
                type=int,
                help='an expansion value for MCL at a range of (1, 5)',
            )
            self.parser.add_argument(
                "--iteration_number", "-itern",
                metavar='iteration_number',
                dest='itern',
                default=100,
                type=int,
                help='int - iteration number for MCL at a range of (1, +inf) (100 by defualt)',
            )
            self.parser.add_argument(
                "--mcl_fold_thres", "-fthres",
                metavar='mcl_fold_thres',
                dest='fthres',
                default=1.1,
                type=float,
                help='float - a fold threshold for MCL  at a range of (1, l) where l is the length of a UMI (1.5 by defualt)',
            )
            self.parser.add_argument(
                "--is_sv", "-issv",
                metavar='is_sv',
                dest='issv',
                default=True,
                type=bool,
                help='bool - to make sure if the deduplicated bam info writes to a bam file.',
            )
            self.parser.add_argument(
                "--output_bam", "-obam",
                metavar='output_bam',
                dest='obam',
                # required=True,
                default='None',
                type=str,
                help='str - output deduplicated reads to a bam file.',
            )
            self.parser.add_argument(
                "--output_dedup_sum", "-odsum",
                metavar='output_dedup_sum',
                dest='odsum',
                default='None',
                type=str,
                help='str - output deduplicated statistics (including count matrix) to a file.',
            )
            self.parser.add_argument(
                "--output_ave_ed", "-oaed",
                metavar='output_ave_ed',
                dest='oaed',
                default='None',
                type=str,
                help='str - output statistics of average edit distances to a file.',
            )
            self.parser.add_argument(
                "--verbose", "-vb",
                metavar='verbose',
                dest='vb',
                default=True,
                type=bool,
                help='bool - to enable if output logs are on console, print log on the console, (True by default or False)',
            )
            self.parser.add_argument(
                "--gene_assigned_tag", "-gt",
                metavar='gene_assigned_tag',
                dest='gt',
                required=True,
                type=str,
                help='str - to enable deduplication on the gene tag (XT recommended)',
            )
            self.parser.add_argument(
                "--gene_is_assigned_tag", "-gist",
                metavar='gene_is_assigned_tag',
                dest='gist',
                required=True,
                type=str,
                help='str - to check if reads are assigned the gene tag (XS recommended).',
            )
            args = self.parser.parse_args()
            self.method = args.m
            self.bam_fpn = args.ibam
            self.ed_thres = args.ed
            self.gene_assigned_tag = args.gt
            self.gene_is_assigned_tag = args.gist
            self.mcl_fold_thres = args.fthres
            self.inflat_val = args.infv
            self.exp_val = args.expv
            self.iter_num = args.itern
            self.is_sv = args.issv
            self.sv_fpn = args.obam
            self.sv_dsum_fpn = args.odsum
            self.sv_aed_fpn = args.oaed
            self.verbose = args.vb

        self.console = console()
        self.console.verbose = self.verbose

        self.dirname = os.path.dirname(self.sv_fpn) + './'
        self.umimonoclust = umimonoclust()
        self.umitoolmonoadj = umitoolmonoadj()
        self.umitoolmonodirec = umitoolmonodirec()

        self.alireader = aliread(bam_fpn=self.bam_fpn, verbose=self.verbose)
        self.df_bam = self.alireader.todf(tags=[self.gene_assigned_tag, self.gene_is_assigned_tag])
        self.console.print('======># of raw reads: {}'.format(self.df_bam.shape[0]))
        self.df_bam = self.df_bam.loc[self.df_bam['reference_id'] != -1]
        self.console.print('======># of reads with qualified chrs: {}'.format(self.df_bam.shape[0]))
        self.df_bam = self.df_bam.loc[self.df_bam[self.gene_is_assigned_tag] == 'Assigned']
        # self.df_bam = self.df_bam.loc[self.df_bam[self.gene_is_assigned_tag] == 'Assigned'][:10000]
        self.console.print('======># of reads with assigned genes: {}'.format(self.df_bam.shape[0]))

        self.df_bam['umi'] = self.df_bam['query_name'].apply(lambda x: x.split('_')[1])
        self.df_bam['umi'] = self.df_bam['query_name'].apply(lambda x: self.correct(x))
        self.console.print('======># of unique umis: {}'.format(self.df_bam['umi'].unique().shape[0]))
        self.console.print('======># of redundant umis: {}'.format(self.df_bam['umi'].shape[0]))

        self.aliwriter = aliwrite(df=self.df_bam)
        self.aliwriter.is_sv = self.is_sv

        self.df_bam_gp = self.df_bam.groupby(by=[self.gene_assigned_tag])
        self.gp_keys = self.df_bam_gp.groups.keys()
        self.console.print('======># of gene positions in the bam: {}'.format(len(self.gp_keys)))
        self.console.print('======>edit distance thres: {}'.format(self.ed_thres))

        self.umimonomcl = umimonomcl(
            inflat_val=self.inflat_val,
            exp_val=self.exp_val,
            iter_num=self.iter_num,
        )

        self.console.print('===>start building umi graphs...')
        umi_graph_build_stime = time.time()
        gps = []
        res_sum = []
        for g in self.gp_keys:
            umi_vignette = self.umibuild(
                df=self.df_bam_gp.get_group(g),
                ed_thres=self.ed_thres,
                verbose=False,
                # verbose=True,
            ).data_summary
            # print(umi_vignette)
            # if len(umi_vignette['umi_uniq_mapped_rev']) == 1:
            #     continue
            # else:
            cc = self.umimonoclust.cc(umi_vignette['graph_adj'])
            gps.append(g)
            res_sum.append([
                umi_vignette,
                cc,
                [*umi_vignette['umi_uniq_mapped_rev'].keys()],
            ])
        self.df = pd.DataFrame(
            data=res_sum,
            columns=['vignette', 'cc', 'uniq_repr_nodes'],
            index=gps,
        )
        self.console.print('===>time for building umi graphs: {:.2f}s'.format(time.time() - umi_graph_build_stime))

        self.df['uniq_umi_len'] = self.df['uniq_repr_nodes'].apply(lambda x: self.length(x))

        self.console.print('===>start deduplication by the {} method...'.format(self.method))
        if self.method == 'unique':
            dedup_umi_stime = time.time()
            # self.df['uniq_sgl_mark'] = self.df['uniq_repr_nodes'].apply(lambda x: self.markSingleUMI(x))
            # self.df = self.df.loc[self.df['uniq_sgl_mark'] == 'no']
            self.console.print('======># of positions with non-single umis: {}'.format(self.df.shape[0]))
            self.console.print('======>finish finding deduplicated umis in {:.2f}s'.format(time.time() - dedup_umi_stime))
            self.df['dedup_uniq_diff_pos'] = self.df.apply(lambda x: self.diffDedupUniqCountPos(x, by_col='uniq_repr_nodes'), axis=1)
            self.df['dedup_read_diff_pos'] = self.df.apply(lambda x: self.diffDedupReadCountPos(x, by_col='uniq_repr_nodes'), axis=1)
            self.console.print('======># of deduplicated unique umis {} on the basis of the unique method'.format(self.df['dedup_uniq_diff_pos'].sum()))
            self.console.print('======># of deduplicated reads {} on the basis of the unique method'.format(self.df['dedup_read_diff_pos'].sum()))
            self.console.print('======>calculate average edit distances between umis...')
            dedup_umi_edave_stime = time.time()
            self.df['ave_eds'] = self.df.apply(lambda x: self.edave(x, by_col='uniq_repr_nodes'), axis=1)
            self.console.print('======>finish calculating ave eds in {:.2f}s'.format(time.time() - dedup_umi_edave_stime))

            if self.sv_aed_fpn != 'None':
                self.console.print('======>start writing average edit distances to a file...')
                dedup_aed_write_stime = time.time()
                ave_ed_bins = self.df['ave_eds'].value_counts().sort_index()
                # self.console.check(ave_ed_bins)
                self.gwriter.generic(df=ave_ed_bins, sv_fpn=self.sv_aed_fpn, index=True)
                self.console.print('======>finish writing the average edit distances in {:.2f}s'.format(time.time() - dedup_aed_write_stime))

            if self.sv_dsum_fpn != 'None':
                self.df_dedup_sum = self.df[[
                    'ave_eds',
                    'uniq_umi_len',
                    'dedup_uniq_diff_pos',
                    'dedup_read_diff_pos',
                ]]
                self.console.print('======>start writing summary statistics...')
                dedup_sum_stat_write_stime = time.time()
                self.gwriter.generic(
                    df=self.df_dedup_sum,
                    sv_fpn=self.sv_dsum_fpn,
                    index=True,
                    header=True,
                )
                self.console.print('======>finish writing the summary statistics in {:.2f}s'.format(time.time() - dedup_sum_stat_write_stime))

            if self.sv_fpn != 'None':
                self.console.print('======>start writing deduplicated reads to BAM...')
                dedup_reads_write_stime = time.time()
                self.df['uniq_bam_ids'] = self.df.apply(lambda x: self.bamids(x, by_col='uniq_repr_nodes'), axis=1)
                self.aliwriter.tobam(
                    tobam_fpn=self.sv_fpn,
                    tmpl_bam_fpn=self.bam_fpn,
                    whitelist=self.decompose(list_nd=self.df['uniq_bam_ids'].values),
                )
                self.console.print('======>finish writing in {:.2f}s'.format(time.time() - dedup_reads_write_stime))

        elif self.method == 'cluster':
            dedup_umi_stime = time.time()
            self.df['cc_repr_nodes'] = self.df.apply(lambda x: self.umimax(x, by_col='cc'), axis=1)
            self.df['cc_umi_len'] = self.df['cc_repr_nodes'].apply(lambda x: self.length(x))
            self.console.print('======>finish finding deduplicated umis in {:.2f}s'.format(time.time() - dedup_umi_stime))
            self.df['dedup_uniq_diff_pos'] = self.df.apply(lambda x: self.diffDedupUniqCountPos(x, by_col='cc_repr_nodes'), axis=1)
            self.df['dedup_read_diff_pos'] = self.df.apply(lambda x: self.diffDedupReadCountPos(x, by_col='cc_repr_nodes'), axis=1)
            self.console.print('======># of deduplicated unique umis {} on the basis of the unique method'.format(self.df['dedup_uniq_diff_pos'].sum()))
            self.console.print('======># of deduplicated reads {} on the basis of the unique method'.format(self.df['dedup_read_diff_pos'].sum()))
            self.console.print('======>calculate average edit distances between umis...')
            dedup_umi_edave_stime = time.time()
            self.df['ave_eds'] = self.df.apply(lambda x: self.edave(x, by_col='cc_repr_nodes'), axis=1)
            self.console.print('======>finish calculating ave eds in {:.2f}s'.format(time.time() - dedup_umi_edave_stime))

            if self.sv_aed_fpn != 'None':
                self.console.print('======>start writing average edit distances to a file...')
                dedup_aed_write_stime = time.time()
                ave_ed_bins = self.df['ave_eds'].value_counts().sort_index()
                # self.console.check(ave_ed_bins)
                self.gwriter.generic(df=ave_ed_bins, sv_fpn=self.sv_aed_fpn, index=True)
                self.console.print('======>finish writing the average edit distances in {:.2f}s'.format(time.time() - dedup_aed_write_stime))

            if self.sv_dsum_fpn != 'None':
                self.df_dedup_sum = self.df[[
                    'cc_umi_len',
                    'ave_eds',
                    'uniq_umi_len',
                    'dedup_uniq_diff_pos',
                    'dedup_read_diff_pos',
                ]]
                self.console.print('======>start writing summary statistics...')
                dedup_sum_stat_write_stime = time.time()
                self.gwriter.generic(
                    df=self.df_dedup_sum,
                    sv_fpn=self.sv_dsum_fpn,
                    index=True,
                    header=True,
                )
                self.console.print('======>finish writing the summary statistics in {:.2f}s'.format(time.time() - dedup_sum_stat_write_stime))

            if self.sv_fpn != 'None':
                self.console.print('======>start writing deduplicated reads to BAM...')
                dedup_reads_write_stime = time.time()
                self.df['cc_bam_ids'] = self.df.apply(lambda x: self.bamids(x, by_col='cc_repr_nodes'), axis=1)
                self.aliwriter.tobam(
                    tobam_fpn=self.sv_fpn,
                    tmpl_bam_fpn=self.bam_fpn,
                    whitelist=self.decompose(list_nd=self.df['cc_bam_ids'].values),
                )
                self.console.print('======>finish writing in {:.2f}s'.format(time.time() - dedup_reads_write_stime))

        elif self.method == 'adjacency':
            dedup_umi_stime = time.time()
            self.df['adj'] = self.df.apply(
                lambda x: self.umitoolmonoadj.decompose(
                    cc_sub_dict=self.umitoolmonoadj.umi_tools(
                        connected_components=x['cc'],
                        df_umi_uniq_val_cnt=x['vignette']['df_umi_uniq_val_cnt'],
                        graph_adj=x['vignette']['graph_adj'],
                    )['clusters'],
                ),
                axis=1,
            )
            self.df['adj_repr_nodes'] = self.df.apply(lambda x: self.umimax(x, by_col='adj'), axis=1)
            self.df['adj_umi_len'] = self.df['adj_repr_nodes'].apply(lambda x: self.length(x))
            self.console.print('======>finish finding deduplicated umis in {:.2f}s'.format(time.time() - dedup_umi_stime))
            self.df['dedup_uniq_diff_pos'] = self.df.apply(lambda x: self.diffDedupUniqCountPos(x, by_col='adj_repr_nodes'), axis=1)
            self.df['dedup_read_diff_pos'] = self.df.apply(lambda x: self.diffDedupReadCountPos(x, by_col='adj_repr_nodes'), axis=1)
            self.console.print('======># of deduplicated unique umis {} on the basis of the unique method'.format(self.df['dedup_uniq_diff_pos'].sum()))
            self.console.print('======># of deduplicated reads {} on the basis of the unique method'.format(self.df['dedup_read_diff_pos'].sum()))
            self.console.print('======>calculate average edit distances between umis...')
            dedup_umi_edave_stime = time.time()
            self.df['ave_eds'] = self.df.apply(lambda x: self.edave(x, by_col='adj_repr_nodes'), axis=1)
            self.console.print('======>finish calculating ave eds in {:.2f}s'.format(time.time() - dedup_umi_edave_stime))

            if self.sv_aed_fpn != 'None':
                self.console.print('======>start writing average edit distances to a file...')
                dedup_aed_write_stime = time.time()
                ave_ed_bins = self.df['ave_eds'].value_counts().sort_index()
                # self.console.check(ave_ed_bins)
                self.gwriter.generic(df=ave_ed_bins, sv_fpn=self.sv_aed_fpn, index=True)
                self.console.print('======>finish writing the average edit distances in {:.2f}s'.format(time.time() - dedup_aed_write_stime))

            if self.sv_dsum_fpn != 'None':
                self.df_dedup_sum = self.df[[
                    'adj_umi_len',
                    'ave_eds',
                    'uniq_umi_len',
                    'dedup_uniq_diff_pos',
                    'dedup_read_diff_pos',
                ]]
                self.console.print('======>start writing summary statistics...')
                dedup_sum_stat_write_stime = time.time()
                self.gwriter.generic(
                    df=self.df_dedup_sum,
                    sv_fpn=self.sv_dsum_fpn,
                    index=True,
                    header=True,
                )
                self.console.print('======>finish writing the summary statistics in {:.2f}s'.format(time.time() - dedup_sum_stat_write_stime))

            if self.sv_fpn != 'None':
                self.console.print('======>start writing deduplicated reads to BAM...')
                dedup_reads_write_stime = time.time()
                self.df['adj_bam_ids'] = self.df.apply(lambda x: self.bamids(x, by_col='adj_repr_nodes'), axis=1)
                self.aliwriter.tobam(
                    tobam_fpn=self.sv_fpn,
                    tmpl_bam_fpn=self.bam_fpn,
                    whitelist=self.decompose(list_nd=self.df['adj_bam_ids'].values),
                )
                self.console.print('======>finish writing in {:.2f}s'.format(time.time() - dedup_reads_write_stime))

        elif self.method == 'directional':
            dedup_umi_stime = time.time()
            self.df['direc'] = self.df.apply(
                lambda x: self.umitoolmonodirec.decompose(
                    cc_sub_dict=self.umitoolmonodirec.umi_tools(
                        connected_components=x['cc'],
                        df_umi_uniq_val_cnt=x['vignette']['df_umi_uniq_val_cnt'],
                        graph_adj=x['vignette']['graph_adj'],
                    )['clusters'],
                ),
                axis=1,
            )
            self.df['direc_repr_nodes'] = self.df.apply(lambda x: self.umimax(x, by_col='direc'), axis=1)
            self.df['direc_umi_len'] = self.df['direc_repr_nodes'].apply(lambda x: self.length(x))
            self.console.print('======>finish finding deduplicated umis in {:.2f}s'.format(time.time() - dedup_umi_stime))
            self.df['dedup_uniq_diff_pos'] = self.df.apply(lambda x: self.diffDedupUniqCountPos(x, by_col='direc_repr_nodes'), axis=1)
            self.df['dedup_read_diff_pos'] = self.df.apply(lambda x: self.diffDedupReadCountPos(x, by_col='direc_repr_nodes'), axis=1)
            self.console.print('======># of deduplicated unique umis: {} based on the unique method'.format(self.df['dedup_uniq_diff_pos'].sum()))
            self.console.print('======># of deduplicated reads: {} based on the unique method'.format(self.df['dedup_read_diff_pos'].sum()))
            self.console.print('======>calculate average edit distances between umis...')
            dedup_umi_edave_stime = time.time()
            self.df['ave_eds'] = self.df.apply(lambda x: self.edave(x, by_col='direc_repr_nodes'), axis=1)
            self.console.print('======>finish calculating ave eds in {:.2f}s'.format(time.time() - dedup_umi_edave_stime))

            if self.sv_aed_fpn != 'None':
                self.console.print('======>start writing average edit distances to a file...')
                dedup_aed_write_stime = time.time()
                ave_ed_bins = self.df['ave_eds'].value_counts().sort_index()
                # self.console.check(ave_ed_bins)
                self.gwriter.generic(df=ave_ed_bins, sv_fpn=self.sv_aed_fpn, index=True)
                self.console.print('======>finish writing the average edit distances in {:.2f}s'.format(time.time() - dedup_aed_write_stime))

            if self.sv_dsum_fpn != 'None':
                self.df_dedup_sum = self.df[[
                    'direc_umi_len',
                    'ave_eds',
                    'uniq_umi_len',
                    'dedup_uniq_diff_pos',
                    'dedup_read_diff_pos',
                ]]
                self.console.print('======>start writing summary statistics...')
                dedup_sum_stat_write_stime = time.time()
                self.gwriter.generic(
                    df=self.df_dedup_sum,
                    sv_fpn=self.sv_dsum_fpn,
                    index=True,
                    header=True,
                )
                self.console.print('======>finish writing the summary statistics in {:.2f}s'.format(time.time() - dedup_sum_stat_write_stime))

            if self.sv_fpn != 'None':
                self.console.print('======>start writing deduplicated reads to BAM...')
                dedup_reads_write_stime = time.time()
                self.df['direc_bam_ids'] = self.df.apply(lambda x: self.bamids(x, by_col='direc_repr_nodes'), axis=1)
                self.aliwriter.tobam(
                    tobam_fpn=self.sv_fpn,
                    tmpl_bam_fpn=self.bam_fpn,
                    whitelist=self.decompose(list_nd=self.df['direc_bam_ids'].values),
                )
                self.console.print('======>finish writing in {:.2f}s'.format(time.time() - dedup_reads_write_stime))

        elif self.method == 'mcl':
            dedup_umi_stime = time.time()
            self.df['mcl'] = self.df.apply(
                lambda x: self.umimonomcl.decompose(
                    list_nd=self.umimonomcl.dfclusters(
                        connected_components=x['cc'],
                        graph_adj=x['vignette']['graph_adj'],
                    )['clusters'].values,
                ),
                axis=1,
            )
            self.df['mcl_repr_nodes'] = self.df.apply(lambda x: self.umimax(x, by_col='mcl'), axis=1)
            self.df['mcl_umi_len'] = self.df['mcl_repr_nodes'].apply(lambda x: self.length(x))
            self.console.print('======>finish finding deduplicated umis in {:.2f}s'.format(time.time() - dedup_umi_stime))
            self.df['dedup_uniq_diff_pos'] = self.df.apply(lambda x: self.diffDedupUniqCountPos(x, by_col='mcl_repr_nodes'), axis=1)
            self.df['dedup_read_diff_pos'] = self.df.apply(lambda x: self.diffDedupReadCountPos(x, by_col='mcl_repr_nodes'), axis=1)
            self.console.print('======># of deduplicated unique umis: {} based on the unique method'.format(self.df['dedup_uniq_diff_pos'].sum()))
            self.console.print('======># of deduplicated reads: {} based on the unique method'.format(self.df['dedup_read_diff_pos'].sum()))
            self.console.print('======>calculate average edit distances between umis...')
            dedup_umi_edave_stime = time.time()
            self.df['ave_eds'] = self.df.apply(lambda x: self.edave(x, by_col='mcl_repr_nodes'), axis=1)
            self.console.print('======>finish calculating ave eds in {:.2f}s'.format(time.time() - dedup_umi_edave_stime))

            if self.sv_aed_fpn != 'None':
                self.console.print('======>start writing average edit distances to a file...')
                dedup_aed_write_stime = time.time()
                ave_ed_bins = self.df['ave_eds'].value_counts().sort_index()
                # self.console.check(ave_ed_bins)
                self.gwriter.generic(df=ave_ed_bins, sv_fpn=self.sv_aed_fpn, index=True)
                self.console.print('======>finish writing the average edit distances in {:.2f}s'.format(time.time() - dedup_aed_write_stime))

            if self.sv_dsum_fpn != 'None':
                self.df_dedup_sum = self.df[[
                    'mcl_umi_len',
                    'ave_eds',
                    'uniq_umi_len',
                    'dedup_uniq_diff_pos',
                    'dedup_read_diff_pos',
                ]]
                self.console.print('======>start writing summary statistics...')
                dedup_sum_stat_write_stime = time.time()
                self.gwriter.generic(
                    df=self.df_dedup_sum,
                    sv_fpn=self.sv_dsum_fpn,
                    index=True,
                    header=True,
                )
                self.console.print('======>finish writing the summary statistics in {:.2f}s'.format(time.time() - dedup_sum_stat_write_stime))

            if self.sv_fpn != 'None':
                self.console.print('======>start writing deduplicated reads to BAM...')
                dedup_reads_write_stime = time.time()
                self.df['mcl_bam_ids'] = self.df.apply(lambda x: self.bamids(x, by_col='mcl_repr_nodes'), axis=1)
                self.aliwriter.tobam(
                    tobam_fpn=self.sv_fpn,
                    tmpl_bam_fpn=self.bam_fpn,
                    whitelist=self.decompose(list_nd=self.df['mcl_bam_ids'].values),
                )
                self.console.print('======>finish writing in {:.2f}s'.format(time.time() - dedup_reads_write_stime))

        elif self.method == 'mcl_val':
            dedup_umi_stime = time.time()
            self.df['mcl_val'] = self.df.apply(
                lambda x: self.umimonomcl.decompose(
                    list_nd=self.umimonomcl.maxval_val(
                        df_mcl_ccs=self.umimonomcl.dfclusters(
                            connected_components=x['cc'],
                            graph_adj=x['vignette']['graph_adj'],
                        ),
                        df_umi_uniq_val_cnt=x['vignette']['df_umi_uniq_val_cnt'],
                        thres_fold=self.mcl_fold_thres,
                    )['clusters'].values,
                ),
                axis=1,
            )
            self.df['mcl_val_repr_nodes'] = self.df.apply(lambda x: self.umimax(x, by_col='mcl_val'), axis=1)
            self.df['mcl_val_umi_len'] = self.df['mcl_val_repr_nodes'].apply(lambda x: self.length(x))
            self.console.print('======>finish finding deduplicated umis in {:.2f}s'.format(time.time() - dedup_umi_stime))
            self.df['dedup_uniq_diff_pos'] = self.df.apply(lambda x: self.diffDedupUniqCountPos(x, by_col='mcl_val_repr_nodes'), axis=1)
            self.df['dedup_read_diff_pos'] = self.df.apply(lambda x: self.diffDedupReadCountPos(x, by_col='mcl_val_repr_nodes'), axis=1)
            self.console.print('======># of deduplicated unique umis: {}, based on the mcl_ed method'.format(self.df['dedup_uniq_diff_pos'].sum()))
            self.console.print('======># of deduplicated reads: {} based on the unique method'.format(self.df['dedup_read_diff_pos'].sum()))
            self.console.print('======>calculate average edit distances between umis...')
            dedup_umi_edave_stime = time.time()
            self.df['ave_eds'] = self.df.apply(lambda x: self.edave(x, by_col='mcl_val_repr_nodes'), axis=1)
            self.console.print('======>finish calculating ave eds in {:.2f}s'.format(time.time() - dedup_umi_edave_stime))

            if self.sv_aed_fpn != 'None':
                self.console.print('======>start writing average edit distances to a file...')
                dedup_aed_write_stime = time.time()
                ave_ed_bins = self.df['ave_eds'].value_counts().sort_index()
                # self.console.check(ave_ed_bins)
                self.gwriter.generic(df=ave_ed_bins, sv_fpn=self.sv_aed_fpn, index=True)
                self.console.print('======>finish writing the average edit distances in {:.2f}s'.format(time.time() - dedup_aed_write_stime))

            if self.sv_dsum_fpn != 'None':
                self.df_dedup_sum = self.df[[
                    'mcl_val_umi_len',
                    'ave_eds',
                    'uniq_umi_len',
                    'dedup_uniq_diff_pos',
                    'dedup_read_diff_pos',
                ]]
                self.console.print('======>start writing summary statistics...')
                dedup_sum_stat_write_stime = time.time()
                self.gwriter.generic(
                    df=self.df_dedup_sum,
                    sv_fpn=self.sv_dsum_fpn,
                    index=True,
                    header=True,
                )
                self.console.print('======>finish writing the summary statistics in {:.2f}s'.format(time.time() - dedup_sum_stat_write_stime))

            if self.sv_fpn != 'None':
                self.console.print('======>start writing deduplicated reads to BAM...')
                dedup_reads_write_stime = time.time()
                self.df['mcl_val_bam_ids'] = self.df.apply(lambda x: self.bamids(x, by_col='mcl_val_repr_nodes'), axis=1)
                self.aliwriter.tobam(
                    tobam_fpn=self.sv_fpn,
                    tmpl_bam_fpn=self.bam_fpn,
                    whitelist=self.decompose(list_nd=self.df['mcl_val_bam_ids'].values),
                )
                self.console.print('======>finish writing in {:.2f}s'.format(time.time() - dedup_reads_write_stime))

        elif self.method == 'mcl_ed':
            dedup_umi_stime = time.time()
            self.df['mcl_ed'] = self.df.apply(
                lambda x: self.umimonomcl.decompose(
                    list_nd=self.umimonomcl.maxval_ed(
                        df_mcl_ccs=self.umimonomcl.dfclusters(
                            connected_components=x['cc'],
                            graph_adj=x['vignette']['graph_adj'],
                        ),
                        df_umi_uniq_val_cnt=x['vignette']['df_umi_uniq_val_cnt'],
                        umi_uniq_mapped_rev=x['vignette']['umi_uniq_mapped_rev'],
                        thres_fold=self.mcl_fold_thres,
                    )['clusters'].values,
                ),
                axis=1,
            )
            self.df['mcl_ed_repr_nodes'] = self.df.apply(lambda x: self.umimax(x, by_col='mcl_ed'), axis=1)
            self.df['mcl_ed_umi_len'] = self.df['mcl_ed_repr_nodes'].apply(lambda x: self.length(x))
            self.console.print('======>finish finding deduplicated umis in {:.2f}s'.format(time.time() - dedup_umi_stime))
            self.df['dedup_uniq_diff_pos'] = self.df.apply(lambda x: self.diffDedupUniqCountPos(x, by_col='mcl_ed_repr_nodes'), axis=1)
            self.df['dedup_read_diff_pos'] = self.df.apply(lambda x: self.diffDedupReadCountPos(x, by_col='mcl_ed_repr_nodes'), axis=1)
            self.console.print('======># of deduplicated unique umis: {}, based on the mcl_ed method'.format(self.df['dedup_uniq_diff_pos'].sum()))
            self.console.print('======># of deduplicated reads: {}, based on the mcl_ed method'.format(self.df['dedup_read_diff_pos'].sum()))
            self.console.print('======>calculate average edit distances between umis...')
            dedup_umi_edave_stime = time.time()
            self.df['ave_eds'] = self.df.apply(lambda x: self.edave(x, by_col='mcl_ed_repr_nodes'), axis=1)
            self.console.print('======>finish calculating ave eds in {:.2f}s'.format(time.time() - dedup_umi_edave_stime))

            if self.sv_aed_fpn != 'None':
                self.console.print('======>start writing average edit distances to a file...')
                dedup_aed_write_stime = time.time()
                ave_ed_bins = self.df['ave_eds'].value_counts().sort_index()
                # self.console.check(ave_ed_bins)
                self.gwriter.generic(df=ave_ed_bins, sv_fpn=self.sv_aed_fpn, index=True)
                self.console.print('======>finish writing the average edit distances in {:.2f}s'.format(time.time() - dedup_aed_write_stime))

            if self.sv_dsum_fpn != 'None':
                self.df_dedup_sum = self.df[[
                    'mcl_ed_umi_len',
                    'ave_eds',
                    'uniq_umi_len',
                    'dedup_uniq_diff_pos',
                    'dedup_read_diff_pos',
                ]]
                self.console.print('======>start writing summary statistics...')
                dedup_sum_stat_write_stime = time.time()
                self.gwriter.generic(
                    df=self.df_dedup_sum,
                    sv_fpn=self.sv_dsum_fpn,
                    index=True,
                    header=True,
                )
                self.console.print('======>finish writing the summary statistics in {:.2f}s'.format(time.time() - dedup_sum_stat_write_stime))

            if self.sv_fpn != 'None':
                self.console.print('======>start writing deduplicated reads to BAM...')
                dedup_reads_write_stime = time.time()
                self.df['mcl_ed_bam_ids'] = self.df.apply(lambda x: self.bamids(x, by_col='mcl_ed_repr_nodes'), axis=1)
                self.aliwriter.tobam(
                    tobam_fpn=self.sv_fpn,
                    tmpl_bam_fpn=self.bam_fpn,
                    whitelist=self.decompose(list_nd=self.df['mcl_ed_bam_ids'].values),
                )
                self.console.print('======>finish writing the bam in {:.2f}s'.format(time.time() - dedup_reads_write_stime))

        # sys.stdout.close()

    def diffDedupUniqCountPos(self, df_row, by_col):
        return df_row['uniq_umi_len'] - len(df_row[by_col])

    def diffDedupReadCountPos(self, df_row, by_col):
        diff_nodes = set(df_row['uniq_repr_nodes']) - set(df_row[by_col])
        if diff_nodes != set():
            # print(diff_nodes)
            umi_val_cnt_dict = df_row['vignette']['df_umi_uniq_val_cnt'].to_dict()
            # print(umi_val_cnt_dict)
            return sum(umi_val_cnt_dict[node] for node in diff_nodes)
        else:
            return 0

    def length(self, df_val):
        return len(df_val)

    def markSingleUMI(self, df_val):
        if len(df_val) == 1:
            return 'yes'
        else:
            return 'no'

    def correct(self, umi):
        vernier = [i for i in range(30) if i % 3 == 0]
        umi_trimers = [umi[v: v+3] for v in vernier]
        # umi_trimers = textwrap.wrap(umi, 3)
        t = []
        for umi_trimer in umi_trimers:
            s = set(umi_trimer)
            if len(s) == 3:
                rand_index = self.rannum.uniform(low=0, high=3, num=1, use_seed=False)[0]
                t.append(umi_trimer[rand_index])
            elif len(s) == 2:
                sdict = {umi_trimer.count(i): i for i in s}
                t.append(sdict[2])
            else:
                t.append(umi_trimer[0])
        return ''.join(t)

    def decompose(self, list_nd):
        """

        Parameters
        ----------
        x

        Returns
        -------

        """
        list_md = []
        for i in list_nd:
            list_md = list_md + i
        self.console.print('======># of the total reads left after deduplication: {}'.format(len(list_md)))
        return list_md

    def bamids(self, df_row, by_col):
        """"""
        bam_id_maps = df_row['vignette']['umi_bam_ids']
        list_1d = df_row[by_col]
        return [bam_id_maps[node] for node in list_1d]

    def umimax(self, df_row, by_col):
        umi_val_cnts = df_row['vignette']['df_umi_uniq_val_cnt']
        umi_cc = []
        for k_c, nodes in df_row[by_col].items():
            # self.console.print('cc: ', x['cc'])
            # self.console.print('vc: ', umi_val_cnts)
            # self.console.print('nodes: ',nodes)
            # self.console.print('val_cnts: ', umi_val_cnts.loc[umi_val_cnts.index.isin(nodes)].max())
            umi_max = umi_val_cnts.loc[umi_val_cnts.index.isin(nodes)].idxmax()
            umi_cc.append(umi_max)
            # self.console.print('val_cnts1: ',)
        return umi_cc

    def edave(self, df_row, by_col):
        repr_nodes = df_row[by_col]
        umi_maps = df_row['vignette']['umi_uniq_mapped_rev']
        node_len = len(repr_nodes)
        if node_len != 1:
            ed_list = []
            for i in range(node_len):
                for j in range(i + 1, node_len):
                    ed_list.append(hamming().general(
                        s1=umi_maps[repr_nodes[i]],
                        s2=umi_maps[repr_nodes[j]],
                    ))
            return np.ceil(sum(ed_list) / (len(ed_list)))
        else:
            return -1

    def eds_(self, df_row, by_col):
        """"""
        print(df_row.index)
        repr_nodes = df_row[by_col]
        umi_maps = df_row['vignette']['umi_uniq_mapped_rev']
        umi_val_cnts = df_row['vignette']['df_umi_uniq_val_cnt']
        # print(repr_nodes)
        # if len(repr_nodes) == len(np.unique(repr_nodes)):
        #     print(True)
        # else:
        #     print(False)
        node_len = len(repr_nodes)
        if node_len != 1:
            ed_list = []
            for i in range(node_len):
                for j in range(i + 1, node_len):
                    if repr_nodes[i] != repr_nodes[j]:
                        ed_list = ed_list + [hamming().general(
                            umi_maps[repr_nodes[i]],
                            umi_maps[repr_nodes[j]])
                        ] * (umi_val_cnts.loc[repr_nodes[i]] * umi_val_cnts.loc[repr_nodes[j]])
            return round(sum(ed_list) / len(ed_list))
        else:
            return -1

    def evaluate(self, ):
        return


if __name__ == "__main__":
    from mclumi.Path import to

    umikit = dedupGene(
        mode='internal',
        # mode='external',

        # method='unique',
        # method='cluster',
        # method='adjacency',
        # method='directional',
        method='mcl',
        # method='mcl_val',
        # method='mcl_ed',

        bam_fpn=to('example/data/RM82CLK1_S1_XT_gene.bam'),
        gene_assigned_tag='XT',
        gene_is_assigned_tag='XS',
        mcl_fold_thres=1.6,
        inflat_val=1.6,
        exp_val=2,
        iter_num=100,
        verbose=True,
        ed_thres=7,
        is_sv=False,
        sv_fpn=to('example/data/RM82CLK1_S1_XT_gene_dedup.bam'),
        sv_dsum_fpn=to('example/data/RM82CLK1_S1_XT_gene_dedup.txt'),
    )