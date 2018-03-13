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


    def get_root_graph(self):
        return self.__btz_graph


    def get_clusters(self):
        clusters = []
        for node in self.nodes():
            clusters.append(self.nodes[node]['cluster_graph'])
        return clusters


    def __create_clusters_spectral(self):
        sparse_matrix = nx.to_scipy_sparse_matrix(self.__btz_graph)
        spectral = cluster.SpectralClustering(n_clusters=self.__clusters_count,
                                              affinity="precomputed",
                                              n_init=self.__n_init,
                                              degree=self.__degree)
        spectral.fit(sparse_matrix)
        cluster_model_result = spectral.labels_
        return cluster_model_result


    def __create_clusters_nodes(self, cluster_model_result):
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
        return clusters_nodes


    def __print_clusters(self):
        clusters = self.get_clusters()

        for cluster_index, bartez_cluster in enumerate(clusters):
            cluster_nodes = bartez_cluster.nodes()
            print("cluster # " + str(cluster_index))
            for node in cluster_nodes:
                entry = self.__btz_entries[node]
                print("  " + str(node) + " (" + entry.description() + ")")


    def make_clusters(self):
        cluster_model_result = self.__create_clusters_spectral()
        clusters_nodes = self.__create_clusters_nodes(cluster_model_result)

        # entries_as_np_array, from np to select a list from another: list = list1[list2]
        entries_as_np_array = np.array(self.__btz_entries)
        nodes_as_np_array = np.array(self.__btz_graph.nodes())

        # creating nodes containing a BartezCluster
        for cluster_nodes_index, cluster_nodes in enumerate(clusters_nodes):
            cluster_entries = entries_as_np_array[cluster_nodes]

            cluster_as_bon = nodes_as_np_array[cluster_nodes]
            self.add_node(cluster_nodes_index,
                          desc=str(cluster_nodes_index),
                          cluster_bartez=BartezCluster(cluster_entries),
                          cluster_graph=self.__btz_graph.subgraph(cluster_as_bon))

        self.__print_clusters()
        self.__print_clusters_edges()
        self.__create_clusters_edges()


    def __get_relations_as_entries(self, node, entries):
        relations_as_entries = []
        entry = entries[node]
        relations = entry.get_relations()
        for relation in relations:
            relation_entry_index = relation.get_index()
            relations_as_entries.append(entries[relation_entry_index])
        return relations_as_entries


    def __get_relations_as_entries_index(self, node, entries):
        relations_as_entries_index = []
        entry = entries[node]
        relations = entry.get_relations()
        for relation in relations:
            relation_entry_index = relation.get_index()
            relations_as_entries_index.append(relation_entry_index)
        return relations_as_entries_index


    def __print_clusters_edges(self):
        clusters = self.get_clusters()

        print("\n")

        for cluster_index, bartez_cluster in enumerate(clusters):
            cluster_nodes = bartez_cluster.nodes()

            for node in cluster_nodes:
                relations_as_entries_index = self.__get_relations_as_entries_index(node, self.__btz_entries)

                for cluster_other_index, cluser_other in enumerate(clusters):
                    if cluster_index == cluster_other_index:
                        continue

                    other_entries_index = [n for n in cluser_other.nodes()]
                    common_nodes = [r for r in relations_as_entries_index if r in other_entries_index]
                    if len(common_nodes) == 0:
                        # skipping, no common nodes
                        continue

                    print("node " + str(node) + " in cluster (" + str(cluster_index) + ") "
                          "has edge(s) with another cluster (" + str(cluster_other_index) + ")")

                    for common_node in common_nodes:
                        entry = self.__btz_entries[node]
                        common_entry = self.__btz_entries[common_node]
                        print ("  " + str(node) + " ("+entry.description()+") -> "
                                    + str(common_node) + " ("+common_entry.description()+")")
                    print("\n")


    def __create_clusters_edges(self):
        clusters = self.get_clusters()

        for cluster_index, bartez_cluster in enumerate(clusters):
            cluster_nodes = bartez_cluster.nodes()

            for node_index, node in enumerate(cluster_nodes):
                relations_as_entries_index = self.__get_relations_as_entries_index(node, self.__btz_entries)

                for cluster_other_index, cluster_other in enumerate(clusters):
                    if cluster_index == cluster_other_index:
                        continue

                    other_entries_index = [n for n in cluster_other.nodes()]
                    common_nodes = [r for r in relations_as_entries_index if r in other_entries_index]
                    if len(common_nodes) == 0:
                        # skipping, no common nodes
                        continue

                    for common_node in np.array(common_nodes):
                        self.add_edge(cluster_index, cluster_other_index,
                                      bartez_source=node,
                                      bartez_target=common_node)
