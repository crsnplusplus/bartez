from copy import deepcopy

class BartezSolverContainerScenario():
    def __init__(self, entries, traverse_order, forbidden, cluster_scenarios):
        self.entries = deepcopy(entries)
        self.traverse_order = traverse_order
        self.forbidden = forbidden
        self.cluster_scenarios = cluster_scenarios

class BartezSolverScenario():
    def __init__(self, entries, graph, used_words, traverse_order, forbidden):
        self.entries = entries
        self.graph = graph
        self.used_words = used_words
        self.traverse_order = traverse_order
        self.forbidden = forbidden

def make_container_scenario(entries, traverse_order, forbidden, cluster_scenarios):
    return BartezSolverContainerScenario(entries, traverse_order, forbidden, cluster_scenarios)

def make_container_replica(scenario):
    return BartezSolverContainerScenario(scenario.entries,
                                         scenario.traverse_order,
                                         deepcopy(scenario.forbidden),
                                         deepcopy(scenario.cluster_scenarios))

def make_scenario(entries, graph, used_words, traverse_order, forbidden):
    return BartezSolverScenario(entries, graph, used_words, traverse_order, forbidden)

def make_replica(scenario):
    return BartezSolverScenario(deepcopy(scenario.entries),
                                scenario.graph,
                                deepcopy(scenario.used_words),
                                scenario.traverse_order,
                                deepcopy(scenario.forbidden))
