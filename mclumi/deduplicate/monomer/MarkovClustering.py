__version__ = "v1.0"
__copyright__ = "Copyright 2021"
__license__ = "MIT"
__lab__ = "Adam Cribbs lab"

import os
import numpy as np
import pandas as pd
import markov_clustering as mc
from mclumi.network.CC import cc as gbfscc
from mclumi.util.Hamming import hamming


class markovClustering(object):

    def __init__(self, inflat_val, exp_val, iter_num):
        self.gbfscc = gbfscc()
        self.inflat_val = inflat_val
        self.exp_val = exp_val
        self.iter_num = iter_num

    def dfclusters(self, connected_components, graph_adj):
        """

        Parameters
        ----------
        connected_components
            connected components in dict format:
            {
                'cc0': [...] # nodes,
                'cc1': [...],
                'cc2': [...],
                ...
                'ccn': [...],
            }
        graph_adj
            the adjacency list of a graph

        Returns
        -------
            a pandas dataframe
            each connected component is decomposed into more connected subcomponents.

        """
        # print([*connected_components.values])
        df_ccs = pd.DataFrame({'cc': [*connected_components.values()]})
        df_ccs['graph_cc_adj'] = df_ccs['cc'].apply(lambda x: self.graph_cc_adj(x, graph_adj))
        df_ccs['keymap'] = df_ccs['graph_cc_adj'].apply(lambda x: self.keymap(graph_adj=x, reverse=False))
        df_ccs['keymap_rev'] = df_ccs['graph_cc_adj'].apply(lambda x: self.keymap(graph_adj=x, reverse=True))
        df_ccs['cc_adj_mat'] = df_ccs.apply(lambda x: self.matrix(graph_adj=x['graph_cc_adj'], key_map=x['keymap']), axis=1)
        df_ccs['mcl_clusters'] = df_ccs['cc_adj_mat'].apply(lambda x: self.cluster(x))
        df_ccs['clusters'] = df_ccs.apply(lambda x: self.keyToNode(list_2d=x['mcl_clusters'], keymap=x['keymap_rev']), axis=1)
        df_ccs['clust_num'] = df_ccs['clusters'].apply(lambda x: len(x))
        # print(df_ccs[['graph_cc_adj', 'mcl_clusters', 'clusters']])
        # print(df_ccs['clusters'])
        return df_ccs

    def decompose(self, list_nd):
        """

        Parameters
        ----------
        df

        Returns
        -------
        {

        }

        """
        # print(list_nd)
        list_md = []
        for i in list_nd:
            list_md = list_md + i
        res = {}
        for i, cc_sub_each_mcl in enumerate(list_md):
            res[i] = cc_sub_each_mcl
        return res

    def graph_cc_adj(self, cc, graph_adj):
        """

        Parameters
        ----------
        cc
            The first parameter.
        graph_adj
            The se parameter.

        Returns
        -------

        """
        return {node: graph_adj[node] for node in cc}

    def keyToNode(self, list_2d, keymap):
        """

        Parameters
        ----------
        list_2d
        keymap

        Returns
        -------

        """
        return [[keymap[i] for i in lis] for lis in list_2d]

    def cluster(self, cc_adj_mat):
        """

        Parameters
        ----------
        cc_adj_mat

        Returns
        -------

        """
        result = mc.run_mcl(
            cc_adj_mat,
            inflation=self.inflat_val,
            expansion=self.exp_val,
            iterations=int(self.iter_num),
        )
        clusters = mc.get_clusters(result)
        # print(clusters)
        return clusters

    def maxval_val(self, df_mcl_ccs, df_umi_uniq_val_cnt, thres_fold):
        """

        Parameters
        ----------
        df_mcl_ccs
        df_umi_uniq_val_cnt
        thres_fold

        Returns
        -------

        """
        df_mcl_ccs['mscmv_val'] = df_mcl_ccs['clusters'].apply(
            lambda x: self.maxval_val_(
                mcl_clusters_per_cc=x,
                df_umi_uniq_val_cnt=df_umi_uniq_val_cnt,
                thres_fold=thres_fold
            )
        )
        df_mcl_ccs['mscmv_val_len'] = df_mcl_ccs['mscmv_val'].apply(lambda x: x[0])
        df_mcl_ccs['mscmv_val_clusters'] = df_mcl_ccs['mscmv_val'].apply(lambda x: x[1])
        df_mcl_ccs['mscmv_val_apv'] = df_mcl_ccs['mscmv_val'].apply(lambda x: x[2])
        df_mcl_ccs['mscmv_val_disapv'] = df_mcl_ccs['mscmv_val'].apply(lambda x: x[3])
        # print(df_mcl_ccs['mscmv_val_len'].sum())
        # print(df_mcl_ccs[['mscmv_val_clusters', 'mscmv_val_disapv', ]])
        return {
            'count': df_mcl_ccs['mscmv_val_len'],
            'clusters': df_mcl_ccs['mscmv_val_clusters'],
            'apv': df_mcl_ccs['mscmv_val_apv'],
            'disapv': df_mcl_ccs['mscmv_val_disapv'],
        }

    def maxval_val_(self, mcl_clusters_per_cc, df_umi_uniq_val_cnt, thres_fold):
        """

        Parameters
        ----------
        mcl_clusters_per_cc
        df_umi_uniq_val_cnt
        thres_fold

        Returns
        -------

        """
        mcl_sub_clust_max_val_graph = {}
        mcl_sub_clust_max_val_weights = {}
        for clust in mcl_clusters_per_cc:
            cc_clust_sorted = self.sort_vals(df_umi_uniq_val_cnt, cc=clust)
            nodes = [*cc_clust_sorted.keys()]
            weights = [*cc_clust_sorted.values()]
            mcl_sub_clust_max_val_graph[nodes[0]] = set()
            mcl_sub_clust_max_val_weights[nodes[0]] = weights[0]
        # print(mcl_sub_clust_max_val_graph)
        approval = []
        disapproval = []
        mscmv_nodes = [*mcl_sub_clust_max_val_weights.keys()]
        mscmv_weights = [*mcl_sub_clust_max_val_weights.values()]
        mscmv_len = len(mscmv_nodes)
        for i in range(mscmv_len):
            for j in range(i + 1, mscmv_len):
                node_i = mscmv_nodes[i]
                node_j = mscmv_nodes[j]
                node_weight_i = mscmv_weights[i]
                node_weight_j = mscmv_weights[j]
                if node_weight_i > thres_fold * node_weight_j - 1:
                    mcl_sub_clust_max_val_graph[node_i].add(node_j)
                    mcl_sub_clust_max_val_graph[node_j].add(node_i)
                    approval.append([node_i, node_j])
                elif node_weight_j > thres_fold * node_weight_i - 1:
                    mcl_sub_clust_max_val_graph[node_i].add(node_j)
                    mcl_sub_clust_max_val_graph[node_j].add(node_i)
                    approval.append([node_i, node_j])
                else:
                    disapproval.append([node_i, node_j])
        # print(mcl_sub_clust_max_val_graph)
        clusters = list(self.gbfscc.deque(mcl_sub_clust_max_val_graph))
        return len(clusters), clusters, approval, disapproval

    def maxval_ed(self, df_mcl_ccs, df_umi_uniq_val_cnt, umi_uniq_mapped_rev, thres_fold):
        """

        Parameters
        ----------
        df_mcl_ccs
        df_umi_uniq_val_cnt
        umi_uniq_mapped_rev
        thres_fold

        Returns
        -------

        """
        df_mcl_ccs['mscmv_ed'] = df_mcl_ccs['clusters'].apply(
            lambda x: self.maxval_ed_(
                mcl_clusters_per_cc=x,
                df_umi_uniq_val_cnt=df_umi_uniq_val_cnt,
                umi_uniq_mapped_rev=umi_uniq_mapped_rev,
                thres_fold=thres_fold,
            )
        )
        df_mcl_ccs['mscmv_ed_len'] = df_mcl_ccs['mscmv_ed'].apply(lambda x: x[0])
        df_mcl_ccs['mscmv_ed_clusters'] = df_mcl_ccs['mscmv_ed'].apply(lambda x: x[1])
        df_mcl_ccs['mscmv_ed_apv'] = df_mcl_ccs['mscmv_ed'].apply(lambda x: x[2])
        df_mcl_ccs['mscmv_ed_disapv'] = df_mcl_ccs['mscmv_ed'].apply(lambda x: x[3])
        # print(df_mcl_ccs['mscmv_ed_len'].sum())
        # print(df_mcl_ccs[['mscmv_ed_clusters', 'mscmv_ed_disapv', ]])
        return {
            'count': df_mcl_ccs['mscmv_ed_len'],
            'clusters': df_mcl_ccs['mscmv_ed_clusters'],
            'apv': df_mcl_ccs['mscmv_ed_apv'],
            'disapv': df_mcl_ccs['mscmv_ed_disapv'],
        }

    def maxval_ed_(self, mcl_clusters_per_cc, df_umi_uniq_val_cnt, umi_uniq_mapped_rev, thres_fold):
        """
        # for k1, v1 in mcl_sub_clust_max_val_weights.items():
        #     for k2, v2 in mcl_sub_clust_max_val_weights.items():
        #         if k1 != k2:
        #             edh = hamming().general(
        #                 umi_uniq_mapped_rev[k1],
        #                 umi_uniq_mapped_rev[k2],
        #             )
        #             if edh <= thres_fold:
        #                 mcl_sub_clust_max_val_graph[k1].add(k2)
        #                 mcl_sub_clust_max_val_graph[k2].add(k1)
        #                 approval.append([k1, k2])
        #             else:
        #                 disapproval.append([k1, k2])

        Parameters
        ----------
        mcl_clusters_per_cc
        df_umi_uniq_val_cnt
        umi_uniq_mapped_rev
        thres_fold

        Returns
        -------

        """
        mcl_sub_clust_max_val_graph = {}
        mcl_sub_clust_max_val_weights = {}
        for clust in mcl_clusters_per_cc:
            cc_clust_sorted = self.sort_vals(df_umi_uniq_val_cnt, cc=clust)
            nodes = [*cc_clust_sorted.keys()]
            weights = [*cc_clust_sorted.values()]
            mcl_sub_clust_max_val_graph[nodes[0]] = set()
            mcl_sub_clust_max_val_weights[nodes[0]] = weights[0]
        # print(mcl_sub_clust_max_val_graph)
        approval = []
        disapproval = []
        mscmv_nodes = [*mcl_sub_clust_max_val_graph.keys()]
        mscmv_len = len(mscmv_nodes)
        for i in range(mscmv_len):
            for j in range(i + 1, mscmv_len):
                node_i = mscmv_nodes[i]
                node_j = mscmv_nodes[j]
                edh = hamming().general(
                    umi_uniq_mapped_rev[node_i],
                    umi_uniq_mapped_rev[node_j],
                )
                if edh <= thres_fold:
                    mcl_sub_clust_max_val_graph[node_i].add(node_j)
                    mcl_sub_clust_max_val_graph[node_j].add(node_i)
                    approval.append([node_i, node_j])
                else:
                    disapproval.append([node_i, node_j])
        # print(mcl_sub_clust_max_val_graph)
        clusters = list(self.gbfscc.deque(mcl_sub_clust_max_val_graph))
        return len(clusters), clusters, approval, disapproval

    def sort_vals(self, df_umi_uniq_val_cnt, cc):
        """

        Parameters
        ----------
        df_umi_uniq_val_cnt
        cc

        Returns
        -------

        """
        return df_umi_uniq_val_cnt.loc[df_umi_uniq_val_cnt.index.isin(cc)].sort_values(ascending=False).to_dict()

    def keymap(self, graph_adj, reverse=False):
        """

        Parameters
        ----------
        graph_adj
        reverse

        Returns
        -------

        """
        keys = [*graph_adj.keys()]
        glen = len(keys)
        if reverse:
            return {k: keys[k] for k in range(glen)}
        else:
            return {keys[k]: k for k in range(glen)}

    def matrix(self, graph_adj, key_map):
        """

        Parameters
        ----------
        graph_adj
        key_map

        Returns
        -------

        """
        adj_mat = np.zeros(shape=[len(key_map), len(key_map)])
        for k, vals in graph_adj.items():
            for val in vals:
                adj_mat[key_map[k], key_map[val]] = 1
        return adj_mat