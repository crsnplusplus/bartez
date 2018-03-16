import networkx as nx

from bartez.solver.solver_observer import BartezObservable
from bartez.solver.solver_scenario import make_scenario
from bartez.graph.cluster_visitor import BartezClusterVisitorSolver

from copy import deepcopy

class BartezClusterSolver(BartezObservable):
    def __init__(self, container, container_entries, cluster_index, cluster, cluster_entries=None, matcher=None):
        BartezObservable.__init__(self)
        self.__container = container
        self.__container_entries = container_entries

        self.__cluster_index = cluster_index
        self.__cluster_graph = cluster

        self.__entries = cluster_entries
        self.__matcher = matcher

        self.__traverse_order = []
        self.__first_entry_index = 0

    def get_cluster_index(self):
        return self.__cluster_index

    def set_matcher(self, matcher):
        self.__matcher = matcher

    def set_entries(self, entries):
        self.__entries = entries

    def get_entries(self):
        return self.__entries

    def set_first_entry_index(self, first_entry_index):
        self.__first_entry_index = first_entry_index

    def get_num_of_vertex(self):
        return 0 if self.__cluster_graph is None else len(self.__cluster_graph.nodes())

    def run_visitor(self, container_scenario):
        cluster_graph = self.__cluster_graph
        solver = BartezClusterVisitorSolver(self.__matcher)

        for o in self.get_observers():
            solver.register_observer(o)

        used_words = []
        traverse_order = self.__get_traverse_order()
        scenario = make_scenario(deepcopy(self.__container_entries),
                                 self.__cluster_graph,
                                 deepcopy(used_words),
                                 deepcopy(traverse_order),
                                 deepcopy(container_scenario.forbidden))

        first_node_index = traverse_order[0]
        first_traverse_node = cluster_graph.nodes[first_node_index]

        start_node = first_traverse_node['bartez_node']
        cluster_scenario_result, result = self.__back_track_visit(start_node, scenario, solver)

        for o in self.get_observers():
            solver.unregister_observer(o)

        container_scenario_result = deepcopy(container_scenario)
        container_scenario_result.entries = deepcopy(cluster_scenario_result.entries)
        container_scenario_result.forbidden = deepcopy(cluster_scenario_result.forbidden)
        return container_scenario_result, result


    def __back_track_visit(self, node, scenario, solver):
        #replica = make_replica(scenario)
        result_scenario, result = node.accept(solver, scenario)
        return result_scenario, result

    def __get_first_entry(self):
        start = self.__first_entry_index
        #entry_index = self.__entries[start]
        return start

    def __get_traverse_order(self):
        #dfs = nx.dfs_tree(self.__graph, self.__get_first_entry())
        dfs = self.__cluster_graph
        dfs_to = list(nx.dfs_preorder_nodes(dfs))
        return dfs_to
