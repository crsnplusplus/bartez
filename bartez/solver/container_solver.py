from bartez.solver.cluster_solver import *
from bartez.solver.solver_observer import BartezObservable
from bartez.solver.solver_scenario import make_container_scenario, make_container_replica, BartezSolverContainerScenario
from copy import deepcopy


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

    def get_next_cluster_index(self, cluster_index, scenario):
        if self.has_next_cluster(cluster_index, scenario) is False:
            return None

        cluster_pos = scenario.traverse_order.index(cluster_index)
        return scenario.traverse_order[cluster_pos + 1]

    def has_next_cluster(self, cluster_index, scenario):
        assert(cluster_index in scenario.traverse_order)
        cluster_pos = scenario.traverse_order.index(cluster_index)
        return cluster_pos + 1 < len(scenario.traverse_order)

    def run(self):
        first_cluster = self.__get_first_cluster()
        self.__traverse_order = self.__get_container_traverse_order(first_cluster)
        forbidden = []
        cluster_scenarios = {}
        scenario =  make_container_scenario(self.__entries, self.__traverse_order, forbidden, cluster_scenarios)
        intersection = [ self.__entries[0] ]
        result_scenario, result = self.__solve_backtracking(self.__traverse_order[0], scenario, intersection)
        return result_scenario, result

    def __solve_backtracking(self, cluster_index, container_scenario, starting_intersection):
        print("Solving cluster: " + str(cluster_index))
        container = self.__container
        cluster_graph = container.nodes[cluster_index]['bartez_cluster']
        cluster_entries = cluster_graph.get_local_entries_as_dict()

        solver = BartezClusterSolver(self.__container,
                                     container_scenario.entries,
                                     cluster_index,
                                     cluster_graph,
                                     cluster_entries,
                                     self.__matcher)

        self.__register_observers_in_cluster_solver(solver)
        cluster_scenario, visitor_result = solver.run_visitor(container_scenario, starting_intersection)
        self.__unregister_observers_in_cluster_solver(solver)

        container_replica = make_container_replica(container_scenario)

        if visitor_result == False:
            return container_scenario, False

        if self.has_next_cluster(cluster_index, cluster_scenario) is False:
            return cluster_scenario, True # finished

        next_cluster_index = self.get_next_cluster_index(cluster_index, cluster_scenario)
        intersection = self.find_clusters_intersection(cluster_index, next_cluster_index)

        container_replica_staged, replica_result = self.__solve_backtracking(next_cluster_index,
                                                                             container_replica,
                                                                             intersection)
        return container_replica_staged, replica_result

    def __deprecated_run(self):
        first_cluster = self.__get_first_cluster()
        self.__traverse_order = self.__get_container_traverse_order(first_cluster)
        forbidden = []
        scenario = BartezSolverContainerScenario(self.__entries, self.__traverse_order, forbidden)
        intersection = [ self.__entries[0] ]
        result_scenario, result = self.__deprecated_solve_backtracking(self.__traverse_order[0], scenario, intersection)
        return result_scenario, result

    def __deprecated_solve_backtracking(self, cluster_index, scenario, starting_intersection):
        print("Solving cluster: " + str(cluster_index))
        container = self.__container
        cluster_graph = container.nodes[cluster_index]['bartez_cluster']
        cluster_entries = cluster_graph.get_local_entries_as_dict()

        replica = BartezSolverContainerScenario(deepcopy(scenario.entries),
                                                 scenario.traverse_order,
                                                 deepcopy(scenario.forbidden))

        solver = BartezClusterSolver(self.__container,
                                     replica.entries,
                                     cluster_index,
                                     cluster_graph,
                                     cluster_entries,
                                     self.__matcher)

        self.__register_observers_in_cluster_solver(solver)
        result_scenario, visitor_result = solver.run_visitor(replica, starting_intersection)
        self.__unregister_observers_in_cluster_solver(solver)

        if visitor_result == False:
            return scenario, False

        if self.has_next_cluster(cluster_index, result_scenario) is False:
            return result_scenario, True # finished

        next_cluster_index = self.get_next_cluster_index(cluster_index, result_scenario)
        intersection = self.find_clusters_intersection(cluster_index, next_cluster_index)

        if self.__deprecated_solve_backtracking(next_cluster_index, result_scenario, intersection) is True:
            return result_scenario, True

        return scenario, False


    def __register_observers_in_cluster_solver(self, solver):
        for o in self.get_observers():
            solver.register_observer(o)

    def __unregister_observers_in_cluster_solver(self, solver):
        for o in self.get_observers():
            solver.unregister_observer(o)

    def __get_next_cluster(self, index):
        traverse_order = self.__traverse_order
        total_clusters_count = len(traverse_order)
        container = self.__container
        if index + 1 >= total_clusters_count:
            return None

        next_cluster_index = traverse_order[index + 1]
        next_cluster = container.nodes[next_cluster_index]
        return next_cluster

    def find_clusters_intersection(self, c1_index, c2_index):
        if c1_index is None or c2_index is None:
            return None

        container = self.__container
        cluster1_nodes = container.nodes[c1_index]['bartez_cluster'].nodes()
        cluster2_nodes = container.nodes[c2_index]['bartez_cluster'].nodes()

        intersection = []

        for node1 in cluster1_nodes:
            entry = self.__entries[node1]

            for r1 in entry.relations():
                relation = self.__entries[r1.index()]

                if relation.absolute_index() not in cluster2_nodes:
                    continue

                intersection.append(relation)

        return intersection
