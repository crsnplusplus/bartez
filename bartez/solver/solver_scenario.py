def make_scenario(entries, graph, used_words, traverse_order):
    return BartezSolverScenario(entries, graph, used_words, traverse_order)

class BartezSolverScenario():
    def __init__(self, entries, graph, used_words, traverse_order):
        self.entries = entries
        self.graph = graph
        self.used_words = used_words
        self.traverse_order = traverse_order
