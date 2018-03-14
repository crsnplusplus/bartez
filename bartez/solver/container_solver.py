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

    def __solve_backtracking(self, container_entries_as_dict):
        traverse_order = self.__traverse_order
        container = self.__container

        for bartez_cluster_index in traverse_order:
            bartez_cluster = container.nodes[bartez_cluster_index]

            bartez_cluster_node = bartez_cluster['cluster_bartez']
            bartez_cluster_node_graph = bartez_cluster['cluster_graph']

#            if bartez_cluster_node.is_solved():
#                continue

            cluster_entries = bartez_cluster_node.get_entries()
            cluster_entries_as_dict = {}
            for single_entry in cluster_entries:
                cluster_entries_as_dict[single_entry.absolute_index()] = single_entry

            solver = BartezClusterSolver(bartez_cluster_index,
                                         self.__matcher,
                                         cluster_entries_as_dict,
                                         container_entries_as_dict,
                                         bartez_cluster_node_graph)
            self.__register_observers_in_cluster_solver(solver)

            solver.run()

            self.__unregister_observers_in_cluster_solver(solver)

        return True

