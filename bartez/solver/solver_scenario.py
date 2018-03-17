from copy import deepcopy

def make_scenario(entries, graph, used_words, traverse_order, forbidden):
    return BartezSolverScenario(entries, graph, used_words, traverse_order, forbidden)

def make_replica(scenario):
    return BartezSolverScenario(deepcopy(scenario.entries),
                                scenario.graph,
                                deepcopy(scenario.used_words),
                                scenario.traverse_order,
                                deepcopy(scenario.forbidden))

class BartezSolverScenario():
    def __init__(self, entries, graph, used_words, traverse_order, forbidden):
        self.entries = entries
        self.graph = graph
        self.used_words = used_words
        self.traverse_order = traverse_order
        self.forbidden = forbidden
