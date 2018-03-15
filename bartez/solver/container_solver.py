from bartez.solver.cluster_solver import *
from bartez.solver.solver_observer import BartezObservable


class BartezClusterContainerSolver(BartezObservable):
    def __init__(self, entries=None, container=None, matcher=None):
        BartezObservable.__init__(self)
        self.__entries = entries
        self.__container = container
        self.__traverse_order = []
        self.__matcher = matcher

    def set_container(self, container):
        self.__container = container

    def __get_first_cluster(self):
        entries = self.__entries
        container_index = self.__container.find_entry(entries[0])
        return container_index

    def __get_container_traverse_order(self, start):
        bfs = nx.dfs_tree(self.__container, start)
        traverse_order = list(reversed(list(nx.dfs_preorder_nodes(bfs))))
        return traverse_order

    def run(self):
        first_cluster = self.__get_first_cluster()
        self.__traverse_order = self.__get_container_traverse_order(first_cluster)
        self.__solve_backtracking(self.__entries)

    def __register_observers_in_cluster_solver(self, solver):
        for o in self.get_observers():
            solver.register_observer(o)

    def __unregister_observers_in_cluster_solver(self, solver):
        for o in self.get_observers():
            solver.unregister_observer(o)

    def __get_next_cluster(self, index):
        traverse_order = self.__traverse_order
        clusters_count = len(traverse_order)
        container = self.__container
        if index + 1 >= clusters_count:
            return None

        next_cluster_index = traverse_order[index + 1]
        next_cluster = container.nodes[next_cluster_index]
        return next_cluster

    def __find_clusters_intersection(self, cluster1, cluster2):
        if cluster1 is None or cluster2 is None:
            return None

        intersection = []

        cluster1_nodes = cluster1['cluster_graph'].nodes()
        cluster2_nodes = cluster2['cluster_graph'].nodes()

        for node1 in cluster1_nodes:
            entry = self.__entries[node1]

            for r1 in entry.relations():
                relation = self.__entries[r1.index()]

                if relation.absolute_index() not in cluster2_nodes:
                    continue

                intersection.append(relation)

        return intersection


    def __solve_backtracking(self, container_entries_as_dict):
        traverse_order = self.__traverse_order
        container = self.__container

        solved_entries = {}

        for bartez_cluster_index in traverse_order:
            bartez_cluster = container.nodes[bartez_cluster_index]

            next_cluster = self.__get_next_cluster(bartez_cluster_index)
            intersection = self.__find_clusters_intersection(bartez_cluster, next_cluster)
            print(intersection)

            bartez_cluster_node = bartez_cluster['cluster_bartez']
            bartez_cluster_node_graph = bartez_cluster['cluster_graph']

#            if bartez_cluster_node.is_solved():
#                continue

            cluster_entries = bartez_cluster_node.get_local_entries()
            cluster_entries_as_dict = {}
            for single_entry in cluster_entries:
                cluster_entries_as_dict[single_entry.absolute_index()] = single_entry

            solver = BartezClusterSolver(bartez_cluster_index,
                                         self.__matcher,
                                         cluster_entries_as_dict,
                                         container_entries_as_dict,
                                         bartez_cluster_node_graph,
                                         bartez_cluster_node)
            self.__register_observers_in_cluster_solver(solver)

            solver.run_visitor()
            solved_entries = solver.get_entries()
            #container_entries_as_dict

            self.__unregister_observers_in_cluster_solver(solver)

        return True

