from bartez.solver.cluster_solver import *
from bartez.solver.solver_observer import BartezObservable
from copy import copy

class BartezClusterContainerScenario():
    def __init__(self, entries, traverse_order, forbidden):
        self.entries = copy(entries)
        self.traverse_order = copy(traverse_order)
        self.forbidden = forbidden


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

    def get_next_cluster_index(self, cluster_index):
        if self.has_next_cluster(cluster_index) is False:
            return None

        return cluster_index + 1

    def has_next_cluster(self, cluster_index):
        container = self.__container
        next_cluster_index = cluster_index + 1
        clusters_count = len(container.nodes())
        return next_cluster_index < clusters_count

    def run(self):
        first_cluster = self.__get_first_cluster()
        self.__traverse_order = self.__get_container_traverse_order(first_cluster)
        forbidden = []
        scenario = BartezClusterContainerScenario(self.__entries, self.__traverse_order, forbidden)
        return self.__solve_backtracking(self.__traverse_order[0], scenario)

    def __solve_backtracking(self, cluster_index, scenario):
        print("Solving cluster: " + str(cluster_index))
        container = self.__container
        cluster_graph = container.nodes[cluster_index]['bartez_cluster']
        cluster_entries = cluster_graph.get_local_entries_as_dict()

        replica = BartezClusterContainerScenario(scenario.entries,
                                                 scenario.traverse_order,
                                                 scenario.forbidden)

        solver = BartezClusterSolver(self.__container,
                                     replica.entries,
                                     cluster_index,
                                     cluster_graph,
                                     cluster_entries,
                                     self.__matcher)

        self.__register_observers_in_cluster_solver(solver)
        result_scenario, visitor_result = solver.run_visitor(replica)
        self.__unregister_observers_in_cluster_solver(solver)

        if visitor_result == False:
            return False

        if self.has_next_cluster(cluster_index) is False:
            return True # finished

        next_cluster_index = self.get_next_cluster_index(cluster_index)

        if self.__solve_backtracking(next_cluster_index, result_scenario) is True:
            return True

        return False


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
