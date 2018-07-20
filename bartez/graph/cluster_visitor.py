from abc import ABCMeta, abstractmethod

from bartez.solver.solver_observer import BartezObservable
from bartez.solver.solver_scenario import make_replica, BartezForbiddenEntries


class BartezNodeVisitor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def visit_root(self, node, scenario):
        pass

    @abstractmethod
    def visit_node(self, node, scenario):
        pass


class BartezBackJump():
    def __init__(self, source_node, target_node, pattern, from_path):
        self.source_node = source_node
        self.target_node = target_node
        self.pattern = pattern
        self.from_path = from_path


class BartezClusterVisitorSolver(BartezNodeVisitor, BartezObservable):
    __metaclass__ = ABCMeta

    def __init__(self, matcher):
        BartezNodeVisitor.__init__(self)
        BartezObservable.__init__(self)
        self.__matcher = matcher
        self.backjump = None

    def get_children_by_length(self, node, scenario):
        graph = node.get_graph()

        entries = []
        for n in graph.neighbors(node.get_absolute_index()):
            neighbor_entry = scenario.entries[n]
            entries.append((neighbor_entry.get_length(), n, neighbor_entry))

        entries_s = sorted(entries, key=lambda entry : entry[0])
        return [ (x[1], x[2]) for x in entries_s ]

    def get_children_by_topleft_most(self, node, scenario):
        node_index = node.get_absolute_index()
        entry = scenario.entries[node_index]
        entries = entry.get_relations_entries(scenario.entries)
        return entries

    def get_next_child(self, node, scenario):
        graph = node.get_graph()

        if not scenario.path:
            return node

        for path_node_index in scenario.path:
            path_node = graph.nodes()[path_node_index]['bartez_node']

            children = self.get_children_by_topleft_most(path_node, scenario)
            for child_entry in children:
                if child_entry.is_valid() is True:
                    continue

                return graph.nodes()[child_entry.absolute_index()]['bartez_node']

        return None

    def visit_root(self, node, scenario):
        result_scenario, result = self.visit_node(node, scenario)
        return result_scenario, result

    def visit_node(self, node, scenario):
        node_index = node.get_absolute_index()

        entry = scenario.entries[node_index]
        assert(entry.absolute_index() in scenario.node_list)

        pattern = entry.get_pattern(scenario.entries)

        replica = make_replica(scenario)
        entry_replica = replica.entries[entry.absolute_index()]
        entry_replica.set_value(pattern)

        replica.path.append(entry_replica.absolute_index())

        matches = self.__matcher.get_matches(pattern, replica.used_words)

        old_value = entry.get_value()


        matches = list(reversed(sorted(matches)))
#        from random import shuffle
#        shuffle(matches)

        has_matches = len(matches) > 0

        while len(matches) > 0 is True:
            match = matches.pop()
            # trying a match

#            if match in replica.used_words:
#                continue

            entry_replica.set_value(match)
            entry_replica.set_is_valid(True)
            #replica.used_words.append(match)
            self.notify_observers(replica.entries)

            next_node = self.get_next_child(node, replica)
            if next_node is None:
                return replica, True

            forbidden, fw_check = self.forward_check(entry_replica, replica)
            if fw_check is False:
                replica.forbidden = forbidden
                continue

            result_scenario, result = self.visit_node(next_node, replica)

            if result is True:
                return result_scenario, True

            #if match in replica.used_words:
            #    replica.used_words.remove(match)

            entry_replica.set_is_valid(False)
            entry_replica.set_value(old_value)

            if self.backjump is None:
                continue

            if self.backjump.target_node != node_index:
                # backjumping
                return scenario, False

            self.notify_observers_backjump_end(self.backjump, replica, pattern)
            self.backjump = None
            #backjumping complete

        entry_replica.set_is_valid(False)
        entry_replica.set_value(old_value)

        if self.backjump is None:
            self.backjump = self.get_backjump_info(entry_replica, pattern, scenario)

        if self.backjump is not None:
            self.notify_observers_backjump_req(self.backjump, scenario, pattern)

        return scenario, False

    def get_backjump_info(self, entry, pattern, scenario):
#        if pattern.count('.') != 0 and self.__matcher.has_match(pattern):
            # pattern has matches, no need to backjump?
#            return None

        if pattern.count('.') == 0:
            return None

        r_entries = entry.get_relations_entries(scenario.entries)
        r_entries_index = [e.absolute_index() for e in r_entries]
        backjump_to_index = 0

        for path_index in reversed(scenario.path):
            entry_in_path = scenario.entries[path_index]
            entry_in_path_index = entry_in_path.absolute_index()
            if entry_in_path_index in r_entries_index:
                backjump_to_index = entry_in_path_index

                relation_pos = r_entries_index.index(entry_in_path_index)
                new_pattern_list = list(pattern)
#                assert(new_pattern_list[relation_pos] != '.')
                new_pattern_list[relation_pos] = '.'
                new_pattern = "".join(new_pattern_list)

                if self.__matcher.has_match(new_pattern) is True:
                    break

        bj = 0 if backjump_to_index == 0 else scenario.entries[backjump_to_index].absolute_index()
        return BartezBackJump(entry.absolute_index(), bj, pattern, scenario.path)


    def forward_check(self, entry, scenario):
        return self.forward_check_do(entry, scenario, 0, 1)


    def forward_check_do(self, entry, scenario, depth, max_depth):
        if depth >= max_depth:
            return scenario.forbidden, True

        r_entries = entry.get_relations_entries(scenario.entries)

        for e in r_entries:
            if e.is_valid() is True:
                continue

            match = e.get_pattern(scenario.entries)
            if self.__matcher.has_match(match) is False:
                e_index = e.absolute_index()
                scenario.forbidden.add_pattern(e_index, match)
                return scenario.forbidden, False

        for e in r_entries:
            if self.forward_check_do(e, scenario, depth + 1, max_depth) is False:
                return None, False

        return scenario.forbidden, True

    def notify_observers_backjump_end(self, backjump, scenario, pattern):
        message = ( "ending:\n" +
                    "from node " + str(backjump.source_node) +
                    " [" + scenario.entries[backjump.source_node].description() + "]" +
                    " to node " + str(backjump.target_node) + " [" +
                    scenario.entries[backjump.target_node].description() + "]" +
                    " with pattern: " + pattern)

        self.notify_observers_message("backjump end: " + message)

    def notify_observers_backjump_req(self, backjump, scenario, pattern):
        message = ( "requested:\n" +
                    "from node " + str(backjump.source_node) +
                    " [" + scenario.entries[backjump.source_node].description() + "]" +
                    " to node " + str(backjump.target_node) +
                    " [" + scenario.entries[backjump.target_node].description() + "]")
        message += ("\nbackjumping from path: " + str(backjump.from_path) +
                    "\nwith pattern: " + pattern)

        self.notify_observers_message("backjump req: " + message)
