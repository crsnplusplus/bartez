import networkx as nx
import numpy as np

from sklearn import cluster

from bartez.graph.graph import BartezGraph


class BartezCluster(BartezGraph):
    def __init__(self, entries):
        BartezGraph.__init__(self, entries)

    def get_unsatisfied_edges(self):
        unsatisfied_edges = []

        for entry in self.get_entries():
            relations = entry.relations()

            for relation_pos, relation in enumerate(relations):
                relation_entry_index = relation.index()
                cluster_nodes = self.nodes()

                if relation_entry_index in cluster_nodes:
                    continue

                # satisfied / unsatisfied
                unsatisfied_edges.append(relation.index())

        pass

class BartezClusterContainer(nx.Graph):
    def __init__(self, entries, clusters_count, make_clusters=True, n_init=200, degree=20):
        nx.Graph.__init__(self)

        self.__btz_graph = BartezGraph(entries)
        self.__btz_entries = entries
        self.__clusters_count = clusters_count
        self.__n_init = n_init
        self.__degree = degree

        if make_clusters is True:
            self.make_clusters()


    def get_clusters(self):
        clusters = []
        for node in self.nodes():
            clusters.append(self.nodes[node]['cluster_graph'])
        return clusters


    def make_clusters(self):
        # entries_as_np_array, from np to select a list from another: list = list1[list2]
        entries_as_np_array = np.array(self.__btz_entries)
        nodes_as_np_array = np.array(self.__btz_graph.nodes())

        sparse_matrix = nx.to_scipy_sparse_matrix(self.__btz_graph)
        spectral = cluster.SpectralClustering(n_clusters=self.__clusters_count,
                                              affinity="precomputed",
                                              n_init=self.__n_init,
                                              degree=self.__degree)
        spectral.fit(sparse_matrix)
        cluster_model_result = spectral.labels_

        clusters_nodes = []
        # reshaping results to fit in clusters_nodes
        for result_index, cluster_index in enumerate(cluster_model_result):
            if len(clusters_nodes) <= cluster_index:
                while len(clusters_nodes) <= cluster_index:
                    #adding new empty lists
                    clusters_nodes.append([])
                #end while
            #end if
            clusters_nodes[cluster_index].append(result_index)
        #end for

        # creating nodes containing a BartezCluster
        for cluster_nodes_index, cluster_nodes in enumerate(clusters_nodes):
            cluster_entries = entries_as_np_array[cluster_nodes]

            cluster_as_bon = nodes_as_np_array[cluster_nodes]
            self.add_node(cluster_nodes_index,
                          cluster_bartez=BartezCluster(cluster_entries),
                          cluster_graph=self.__btz_graph.subgraph(cluster_as_bon))

        self.__make_clusters_edges()


    def __make_clusters_edges(self):
        btz_nodes = self.__btz_graph.nodes()
        clusters = self.get_clusters()

        for cluster in clusters:
            cluster_nodes = cluster.nodes()

            for cluster2 in clusters:
                if cluster == cluster2:
                    continue

            cluster_nodes2 = cluster.nodes()
            pass


        pass

            # for entry_index, entry in enumerate(nodes):
            #     relations = entry.relations()
            #
            #     for index_relation, relation in enumerate(relations):
            #         relation_index = relation.index()
            #         if relation_index in
            #         self.add_edge(entry_index, relation_index)
            #
            # for node in self.nodes():
            #     node['cluster']
