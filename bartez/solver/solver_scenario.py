from copy import deepcopy

class BartezSolverContainerScenario():
    def __init__(self, entries, traverse_order, forbidden, cluster_scenarios):
        self.entries = entries
        self.traverse_order = traverse_order
        self.forbidden = forbidden
        self.cluster_scenarios = cluster_scenarios

def make_container_scenario(entries, traverse_order, forbidden, cluster_scenarios):
    return BartezSolverContainerScenario(entries, traverse_order, forbidden, cluster_scenarios)

def make_container_replica(scenario):
    return BartezSolverContainerScenario(deepcopy(scenario.entries),
                                         scenario.traverse_order,
                                         deepcopy(scenario.forbidden),
                                         deepcopy(scenario.cluster_scenarios))


class BartezSolverScenario:
    def __init__(self, entries, graph, used_words, node_list, path, forbidden):
        self.entries = entries
        self.graph = graph
        self.used_words = used_words
        self.node_list = node_list
        self.forbidden = forbidden
        self.path = path

def make_scenario(entries, graph, used_words, node_list, path, forbidden):
    return BartezSolverScenario(entries, graph, used_words, node_list, path, forbidden)

def make_replica(scenario):
    return BartezSolverScenario(deepcopy(scenario.entries),
                                scenario.graph,
                                deepcopy(scenario.used_words),
                                scenario.node_list,
                                deepcopy(scenario.path),
                                deepcopy(scenario.forbidden))


class BartezForbiddenEntries:
    def __init__(self):
        self.__pattern = { }

    def add_pattern(self, index, pattern):
        if index not in self.__pattern:
            self.__pattern[index] = set()

        self.__pattern[index].add(pattern)

    def get_patterns(self, index):
        if index not in self.__pattern:
            return None

        return self.__pattern[index]

    def contains_pattern(self, index, pattern):
        if index not in self.__pattern:
            return False

        is_pattern_in_forbidden = pattern in self.__pattern[index]
        return is_pattern_in_forbidden

    def get_all_patterns(self):
        return self.__pattern
