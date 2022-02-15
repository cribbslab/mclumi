import os
import sys
import argparse
import subprocess
from pyfiglet import Figlet


def main():
    parser = argparse.ArgumentParser(description='Welcome to the mclumi toolkit')
    vignette1 = Figlet(font='standard')
    print(vignette1.renderText('MCLUMI Toolkit'))
    vignette2 = Figlet(font='doom')
    print(vignette2.renderText('Welcome'))
    # ## /*** module: trim ***/
    parser.add_argument(
        "tool",
        type=str,
        help='trim, dedup_basic, dedup_pos, dedup_gene, dedup_sc, dechimeric',
    )
    parser.add_argument(
        "--read_structure", "-rs",
        metavar='read_structure',
        dest='rs',
        type=str,
        help='str - the read structure with elements in conjunction with +, e.g., primer_1+umi_1+seq_1+umi_2+primer_2',
    )
    parser.add_argument(
        "--lens", "-l",
        metavar='lens',
        dest='l',
        type=str,
        help='str - lengths of all sub-structures separated by +, e.g., 20+10+40+10+20 if the read structure is primer_1+umi_1+seq_1+umi_2+primer_2',
    )
    parser.add_argument(
        "--input", "-i",
        metavar='input',
        dest='i',
        type=str,
        help='str - input a fastq file in gz format for trimming UMIs',
    )
    parser.add_argument(
        "--output", "-o",
        metavar='output',
        dest='o',
        type=str,
        help='str - output a UMI-trimmed fastq file in gz format.',
    )

    # ## /*** module: dedup_basic ***/
    parser.add_argument(
        "--method", "-m",
        metavar='method',
        dest='m',
        type=str,
        help='str - a dedup method: unique | cluster | adjacency | directional | mcl | mcl_ed | mcl_val | dc_by_cnt',
    )
    parser.add_argument(
        "--input_bam", "-ibam",
        metavar='input_bam',
        dest='ibam',
        type=str,
        help='str - input a bam file curated by requirements of different dedup modules: dedup_basic, dedup_pos, dedup_gene, dedup_sc, dechimeric',
    )
    parser.add_argument(
        "--edit_dist", "-ed",
        metavar='edit dist',
        dest='ed',
        default=1,
        type=int,
        help='int - an edit distance used for building graphs at a range of [1, l) where l is the length of a UMI',
    )
    parser.add_argument(
        "--inflation_value", "-infv",
        metavar='inflation_value',
        dest='infv',
        default=2.0,
        type=float,
        help='float - an inflation value for MCL, 2.0 by default',
    )
    parser.add_argument(
        "--expansion_value", "-expv",
        metavar='expansion_value',
        dest='expv',
        default=2,
        type=int,
        help='int - an expansion value for MCL at a range of (1, +inf), 2 by default',
    )
    parser.add_argument(
        "--iteration_number", "-itern",
        metavar='iteration_number',
        dest='itern',
        default=100,
        type=int,
        help='int - iteration number for MCL at a range of (1, +inf), 100 by default',
    )
    parser.add_argument(
        "--mcl_fold_thres", "-fthres",
        metavar='mcl_fold_thres',
        dest='fthres',
        default=1.1,
        type=float,
        help='float - a fold threshold for MCL at a range of (1, l) where l is the length of a UMI.',
    )
    parser.add_argument(
        "--tc_thres", "-tcthres",
        metavar='tc_thres',
        dest='tcthres',
        default=5,
        type=float,
        help='float - a count threshold for removing chimerical reads made during PCR amplification',
    )
    parser.add_argument(
        "--is_sv", "-issv",
        metavar='is_sv',
        dest='issv',
        default=True,
        type=bool,
        help='bool - to make sure if the deduplicated reads writes to a bam file (True by default or False)',
    )
    parser.add_argument(
        "--output_bam", "-obam",
        metavar='output_bam',
        dest='obam',
        default='None',
        type=str,
        help='str - output a bam file containing UMI-deduplicated or dechimerical reads, or output other summary statistics.',
    )
    parser.add_argument(
        "--output_dedup_sum", "-odsum",
        metavar='output_dedup_sum',
        dest='odsum',
        default='None',
        type=str,
        help='str - output deduplicated statistics (including count matrix) to a file.',
    )
    parser.add_argument(
        "--output_ave_ed", "-oaed",
        metavar='output_ave_ed',
        dest='oaed',
        default='None',
        type=str,
        help='str - output statistics of average edit distances to a file.',
    )
    parser.add_argument(
        "--output_bam_c", "-obam_c",
        metavar='output_bam_c',
        dest='obam_c',
        type=str,
        help='str - output a bam file containing chimerical reads.',
    )
    parser.add_argument(
        "--verbose", "-vb",
        metavar='verbose',
        dest='vb',
        default=True,
        type=bool,
        help='bool - to enable if output logs are on console (True by default or False)',
    )
    parser.add_argument(
        "--pos_tag", "-pt",
        metavar='pos_tag',
        dest='pt',
        type=str,
        help='str - to enable deduplication on the position tags (PO recommended when your bam is tagged)',
    )
    parser.add_argument(
        "--gene_assigned_tag", "-gt",
        metavar='gene_assigned_tag',
        dest='gt',
        type=str,
        help='str - to enable deduplication on the gene tag (XT recommended)',
    )
    parser.add_argument(
        "--gene_is_assigned_tag", "-gist",
        metavar='gene_is_assigned_tag',
        dest='gist',
        type=str,
        help='str - to check if reads are assigned the gene tag (XS recommended)',
    )

    args = parser.parse_args()
    print('The {} module is being used...'.format(args.tool))
    if args.tool == 'trim':
        fpnf = os.path.dirname(__file__) + '/trim/Fixed.py'
        # print(fpnf)
        # cmd = 'python ' + fpnf + ' -h'
        cmd = 'python ' + fpnf + ' -i ' + args.i + ' -o ' + args.o + ' -rs ' + args.rs + ' -l ' + args.l
        # print(cmd)
        s = subprocess.Popen(cmd, shell=True)
        s.communicate()
    if args.tool == 'dedup_basic':
        fpnf = os.path.dirname(__file__) + '/deduplicate/monomer/DedupBasic.py'
        print(fpnf)
        print(args.ibam)
        if args.ibam == None:
            print('Attention! the ibam option must be added to your command for the dedup_basic module.')
            raise ValueError
        if args.ed == None:
            print('Attention! the ed option must be added to your command for the dedup_basic module.')
            raise ValueError
        if args.m == None:
            print('Attention! the m option must be added to your command for the dedup_basic module.')
            raise ValueError
        # cmd = 'python ' + fpnf + ' -h'
        cmd = 'python ' + fpnf + ' -m ' + args.m + ' -ibam ' + args.ibam + ' -ed ' + str(args.ed) + ' -fthres ' + str(args.fthres) + ' -infv ' + str(args.infv) + ' -expv ' + str(args.expv) + ' -itern ' + str(args.itern) + ' -obam ' + args.obam + ' -issv ' + str(args.issv) + ' -vb ' + str(args.vb)
        # print(cmd)
        s = subprocess.Popen(cmd, shell=True)
        s.communicate()
    if args.tool == 'dedup_pos':
        fpnf = os.path.dirname(__file__) + '/deduplicate/monomer/DedupPos.py'
        print(fpnf)

        if args.ibam == None:
            print('Attention! the ibam option must be added to your command for the dedup_pos module.')
            raise ValueError
        if args.ed == None:
            print('Attention! the ed option must be added to your command for the dedup_pos module.')
            raise ValueError
        if args.m == None:
            print('Attention! the m option must be added to your command for the dedup_pos module.')
            raise ValueError
        if args.pt == None:
            print('Attention! the pt option must be added to your command for the dedup_pos module.')
            raise ValueError
        # cmd = 'python ' + fpnf + ' -h'
        cmd = 'python ' + fpnf + ' -m ' + args.m + ' -ibam ' + args.ibam + ' -ed ' + str(args.ed) + ' -pt ' + str(args.pt) + ' -fthres ' + str(args.fthres) + ' -infv ' + str(args.infv) + ' -expv ' + str(args.expv) + ' -itern ' + str(args.itern) + ' -obam ' + args.obam + ' -issv ' + str(args.issv) + ' -vb ' + str(args.vb)
        # print(cmd)
        s = subprocess.Popen(cmd, shell=True)
        s.communicate()
    if args.tool == 'dedup_gene':
        fpnf = os.path.dirname(__file__) + '/deduplicate/monomer/DedupGene.py'
        # print(fpnf)
        if args.ibam == None:
            print('Attention! the ibam option must be added to your command for the dedup_gene module.')
            raise ValueError
        if args.ed == None:
            print('Attention! the ed option must be added to your command for the dedup_gene module.')
            raise ValueError
        if args.m == None:
            print('Attention! the m option must be added to your command for the dedup_gene module.')
            raise ValueError
        if args.gt == None:
            print('Attention! the gene_assigned_tag option must be added to your command for the dedup_gene module.')
            raise ValueError
        if args.gist == None:
            print('Attention! the gene_assigned_tag option must be added to your command for the dedup_gene module.')
            raise ValueError
        # cmd = 'python ' + fpnf + ' -h'
        cmd = 'python ' + fpnf + ' -m ' + args.m + ' -ibam ' + args.ibam + ' -ed ' + str(args.ed) + ' -gt ' + str(args.gt) + ' -gist ' + str(args.gist) + ' -fthres ' + str(args.fthres) + ' -infv ' + str(args.infv) + ' -expv ' + str(args.expv) + ' -itern ' + str(args.itern) + ' -obam ' + args.obam + ' -odsum ' + args.odsum + ' -oaed ' + args.oaed + ' -issv ' + str(args.issv) + ' -vb ' + str(args.vb)
        # print(cmd)
        s = subprocess.Popen(cmd, shell=True)
        s.communicate()
    if args.tool == 'dedup_sc':
        fpnf = os.path.dirname(__file__) + '/deduplicate/monomer/DedupSC.py'
        # print(fpnf)
        if args.ibam == None:
            print('Attention! the ibam option must be added to your command for the dedup_sc module.')
            raise ValueError
        if args.ed == None:
            print('Attention! the ed option must be added to your command for the dedup_sc module.')
            raise ValueError
        if args.m == None:
            print('Attention! the m option must be added to your command for the dedup_sc module.')
            raise ValueError
        if args.gt == None:
            print('Attention! the gene_assigned_tag option must be added to your command for the dedup_sc module.')
            raise ValueError
        if args.gist == None:
            print('Attention! the gene_assigned_tag option must be added to your command for the dedup_sc module.')
            raise ValueError
        # cmd = 'python ' + fpnf + ' -h'
        cmd = 'python ' + fpnf + ' -m ' + args.m + ' -ibam ' + args.ibam + ' -ed ' + str(args.ed) + ' -gt ' + str(args.gt) + ' -gist ' + str(args.gist) + ' -fthres ' + str(args.fthres) + ' -infv ' + str(args.infv) + ' -expv ' + str(args.expv) + ' -itern ' + str(args.itern) + ' -obam ' + args.obam + ' -issv ' + str(args.issv) + ' -vb ' + str(args.vb)
        # print(cmd)
        s = subprocess.Popen(cmd, shell=True)
        s.communicate()
    if args.tool == 'dechimeric':
        fpnf = os.path.dirname(__file__) + '/deduplicate/trimer/Dechimeric.py'
        # print(fpnf)
        if args.ibam == None:
            print('Attention! the ibam option must be added to your command for the dechimeric module.')
            raise ValueError
        if args.m == None:
            print('Attention! the m option must be added to your command for the dechimeric module.')
            raise ValueError
        # cmd = 'python ' + fpnf + ' -h'
        cmd = 'python ' + fpnf + ' -m ' + args.m + ' -ibam ' + args.ibam + ' -tcthres ' + str(args.tcthres) + ' -obam ' + args.obam + ' -obam_c ' + args.obam_c + ' -issv ' + str(args.issv) + ' -vb ' + str(args.vb)
        # print(cmd)
        s = subprocess.Popen(cmd, shell=True)
        s.communicate()