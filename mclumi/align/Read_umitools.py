import umi_tools.sam_methods as sam_methods
import pysam
from mclumi.util.Hamming import hamming
import pandas as pd
import numpy as np
from mclumi.Path import to


def edave(x, d):
    repr_nodes = d[x[1]]
    node_len = len(repr_nodes)
    if node_len != 1:
        ed_list = []
        for i in range(node_len):
            for j in range(i + 1, node_len):
                ed_list.append(hamming().general(
                    s1=repr_nodes[i],
                    s2=repr_nodes[j]
                ))
        return np.ceil(sum(ed_list) / (len(ed_list)))
    else:
        return -1


options = {'stats': 'deduplicated',
           'get_umi_method': 'read_id',
           'umi_sep': '_',
           'umi_tag': 'RX',
           'umi_tag_split': None,
           'umi_tag_delim': None,
           'cell_tag': None,
           'cell_tag_split': '-',
           'cell_tag_delim': None,
           'filter_umi': None,
           'umi_whitelist': None,
           'umi_whitelist_paired': None,
           'method': 'directional',
           'threshold': 1,
           'spliced': False,
           'soft_clip_threshold': 4,
           'read_length': False,
           'per_gene': False,
           'gene_tag': None,
           'assigned_tag': None,
           'skip_regex': '^(__|Unassigned)',
           'per_contig': False,
           'gene_transcript_map': None,
           'per_cell': False,
           'whole_contig': False,
           'detection_method': None,
           'mapping_quality': 0,
           'output_unmapped': False,
           'unmapped_reads': 'discard',
           'chimeric_pairs': 'use',
           'unpaired_reads': 'use',
           'ignore_umi': False,
           'ignore_tlen': False,
           'chrom': None,
           'subset': None,
           'in_sam': False,
           'paired': False,
           'out_sam': False,
           'no_sort_output': False,
           'stdin': "<_io.TextIOWrapper name='example.bam' mode='r' encoding='UTF-8'>",
           'stdlog': "<_io.TextIOWrapper name='<stdout>' mode='w' encoding='UTF-8'>", 'log2stderr': False,
           'compresslevel': 6,
           'timeit_file': None,
           'timeit_name': 'all',
           'timeit_header': None,
           'loglevel': 1,
           'short_help': None,
           'random_seed': None
           }
bundle_iterator = sam_methods.get_bundles(
    options,
    metacontig_contig=None,
)

infile = pysam.Samfile(to('example/data/example.bam'), 'rb')

inreads = infile.fetch()

c = 0
d = []
nInput = 0
tt = []
ttt = []
tttt = []
c_cnt = 0
write_to_bam = pysam.AlignmentFile(to('example/data/example_bundle.bam'), "wb", template=infile)

for i, (bundle, key, status) in enumerate(bundle_iterator(inreads)):
    ttt.append(len(bundle))
    # print([bundle[umi]["read"] for umi in bundle])
    for j, umi in enumerate(bundle):
        bbh = bundle[umi]["read"]
        bbh.set_tag('PO', i)

            # ttt.append(bbh)
        # print(bundle[umi]["read"])
        # write_to_bam.write(bundle[umi]["read"])
        for _ in range(bundle[umi]["count"]):
            tt.append(bundle[umi]["read"])
        c_cnt += 1
    nInput += sum([bundle[umi]["count"] for umi in bundle])
    d.append([i.decode('utf-8') for i in bundle.keys()])
    c += 1

for y in tt:
    write_to_bam.write(y)
print(len(tt))
# print(sum(ttt))
write_to_bam.close()
print(c)
print(len(tttt))
# print(len(np.unique(tttt)))
print('asdasdasd222', nInput)
s = pd.DataFrame(index=np.arange(c))
s[1] = np.arange(c)
s[2] = s.apply(lambda x: edave(x, d), axis=1)
print(s[2])
print(s[2].value_counts())

