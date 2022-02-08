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
from mclumi.deduplicate.monomer.Build import build as umibuild
from mclumi.util.Console import console


class dechimeric():

    def __init__(self, bam_fpn, method, mode='internal', tc_thres=None, is_sv=True, sv_fpn='./dechimerical.bam', verbose=False):
        """
        Parameters
        ----------
        bam_fpn
            str - the full path of a BAM file curated by requirements of different dedup modules
        method
            str - a deduplication method (mcl, mcl_val, mcl_ed, cluster, unique, ajacency, directional)
        mode
            str - externally or internally run the module (external by defualt, internal)
        tc_thres
            float - a count threshold for removing chimerical reads made during PCR amplification
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
            self.tc_thres = tc_thres
            self.is_sv = is_sv
            self.sv_fpn = sv_fpn
            self.verbose = verbose
            print('run Mclumi internally.')
        else:
            self.parser = argparse.ArgumentParser(
                description='The dedupBasic module'
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
                help='str - input a bam file curated by requirements of THE dedup_basic modules',
            )
            self.parser.add_argument(
                "--tc_thres", "-tcthres",
                metavar='tc_thres',
                dest='tcthres',
                default=-1,
                type=float,
                help='float - a count threshold for removing chimerical reads made during PCR amplification',
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
                required=True,
                type=str,
                help='str - output UMI-de-duplicated summary statistics to a bam file.',
            )
            self.parser.add_argument(
                "--verbose", "-vb",
                metavar='verbose',
                dest='vb',
                default=True,
                type=bool,
                help='bool - to enable if output logs are on console, print log on the console, (True by default or False)',
            )
            args = self.parser.parse_args()
            self.method = args.m
            self.tc_thres = args.tcthres
            self.bam_fpn = args.ibam
            self.is_sv = args.issv
            self.sv_fpn = args.obam
            self.verbose = args.vb

        self.console = console()
        self.console.verbose = self.verbose

        self.dirname = os.path.dirname(self.sv_fpn) + '/'
        # sys.stdout = open(self.dirname + self.method + '_log.txt', 'w')

        self.alireader = aliread(bam_fpn=self.bam_fpn, verbose=self.verbose)
        self.df_bam = self.alireader.todf(tags=[])
        self.console.print('======># of raw reads: {}'.format(self.df_bam.shape[0]))
        self.df_bam = self.df_bam.loc[self.df_bam['reference_id'] != -1]
        self.console.print('======># of reads with qualified chrs: {}'.format(self.df_bam.shape[0]))
        # self.df_bam = self.df_bam.loc[self.df_bam[self.gene_is_assigned_tag] == 'Assigned']

        self.df_bam['umi_l'] = self.df_bam['query_name'].apply(lambda x: x.split('_')[1])
        self.df_bam['umi_r'] = self.df_bam['query_name'].apply(lambda x: x.split('_')[2])
        self.df_bam['umi'] = self.df_bam.apply(lambda x: x['umi_l'] + x['umi_r'], axis=1)
        self.cnt_paired_umis = self.df_bam['umi'].value_counts()
        if self.tc_thres == -1:
            self.tc_thres = self.cnt_paired_umis.quantile(.1)
        self.hash_paired_umis = self.cnt_paired_umis.to_dict()
        self.df_bam['chimeric_mark'] = self.df_bam['umi'].apply(lambda x: 1 if self.hash_paired_umis[x] > self.tc_thres else 0)
        self.nonchimerical_ids = self.df_bam['chimeric_mark'].loc[self.df_bam['chimeric_mark'] == 1].index
        self.console.print('======># of chimerical reads detected: {}'.format(self.df_bam.shape[0] - self.nonchimerical_ids.shape[0]))

        self.aliwriter = aliwrite(df=self.df_bam)
        self.aliwriter.is_sv = self.is_sv

        dechimeric_write_stime = time.time()
        self.aliwriter.tobam(
            tobam_fpn=self.dirname + self.method + '_dechimeric.bam',
            tmpl_bam_fpn=self.bam_fpn,
            whitelist=self.decompose(list_nd=self.nonchimerical_ids.values),
        )
        self.console.print('======>finish writing in {:.2f}s'.format(time.time() - dechimeric_write_stime))

    def decompose(self, list_nd):
        list_md = []
        for i in list_nd:
            list_md = list_md + i
        self.console.print('======># of the total reads left after deduplication: {}'.format(len(list_md)))
        return list_md