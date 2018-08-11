from abc import ABCMeta, abstractmethod

from bartez.solver.solver_observer import BartezObservable
from bartez.solver.solver_scenario import make_replica, BartezForbiddenEntries
from bartez.dictionary.trie_node_visitor import BartezDictionaryTrieNodeVisitorMatchPattern
from bartez.entry import get_entries_intersection, get_entries_by_length
import networkx as nx

from copy import deepcopy

class BartezNodeVisitor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def visit_root(self, node, scenario):
        pass

    @abstractmethod
    def visit_node(self, node, scenario):
        pass


class BartezBackJump:
    def __init__(self, source_node, target_node, pattern, from_path, scenario):
        self.source_node = source_node
        self.target_node = target_node
        self.pattern = pattern
        self.from_path = from_path
        self.scenario = deepcopy(scenario)


class BartezClusterVisitorSolver(BartezNodeVisitor, BartezObservable):
    __metaclass__ = ABCMeta

    def __init__(self, matcher):
        BartezNodeVisitor.__init__(self)
        BartezObservable.__init__(self)
        self.__matcher = matcher
        self.backjump = None
        self.traverse_order = []

    def get_children_by_length(self, node, scenario):
        node_index = node.get_absolute_index()
        entry = scenario.entries[node_index]
        entries_ret = entry.get_relations_entries(scenario.entries)
        entries_ret = get_entries_by_length(entries_ret)
        return entries_ret

    def get_children_by_topleft_most(self, node, scenario):
        node_index = node.get_absolute_index()
        entry = scenario.entries[node_index]
        entries = entry.get_relations_entries(scenario.entries)
        return entries

    def get_children_by_bottomright_most(self, node, scenario):
        return reversed(self.get_children_by_topleft_most(node,scenario))

    def get_next_child(self, node, scenario):
        graph = node.get_graph()

        if not scenario.path:
            return node

        node_index = node.get_absolute_index()
        entry = scenario.entries[node_index]

        for path_node_index in scenario.path:
            path_node = graph.nodes()[path_node_index]['bartez_node']

            if entry.is_horizontal() is True:
                children = self.get_children_by_topleft_most(path_node, scenario)
                #children = self.get_children_by_bottomright_most(path_node, scenario)
            else:
                #children = self.get_children_by_bottomright_most(path_node, scenario)
                 children = self.get_children_by_topleft_most(path_node, scenario)
                #children = self.get_children_by_length(path_node, scenario)

            for child_entry in children:
                if child_entry.is_valid() is True:
                    continue

                return graph.nodes()[child_entry.absolute_index()]['bartez_node']

        return None

    def visit_root(self, root, scenario):
        dfs = nx.dfs_tree(root.get_graph(), 0)
        self.traverse_order = list(nx.dfs_preorder_nodes(dfs))
        result_scenario, result = self.visit_node(root, scenario)
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

        matches_tree = self.__matcher.get_matches_tree(pattern, replica.used_words)


        matches = list(reversed(sorted(matches)))
        #from random import shuffle
        #shuffle(matches)

        while (len(matches) > 0) is True:
            match = matches.pop()
            # trying a match

#            if match in replica.used_words:
#                continue

            entry_replica.set_value(match)
            entry_replica.set_is_valid(True)
            replica.used_words.append(match)
            self.notify_observers(replica.entries)

            next_node = self.get_next_child(node, replica)
            if next_node is None:
                return replica, True

            failing_r_vertex, failing_pattern, fw_check = self.forward_check(entry_replica, replica)
            if fw_check is False:
                pattern_to_remove = self.get_failing_pattern(entry_replica, replica, failing_r_vertex)
                matcher = BartezDictionaryTrieNodeVisitorMatchPattern(pattern_to_remove)
                matches_tree.get_root().accept(matcher)
                matches_to_remove = matcher.detach_matches()

                for m in matches_to_remove:
                    if m not in matches:
                        continue
                    matches.remove(m)

                # forward check failed
                continue

            result_scenario, result = self.visit_node(next_node, replica)

            if result is True:
                return result_scenario, True

            if match in replica.used_words:
                replica.used_words.remove(match)

            entry_replica.set_is_valid(False)
            entry_replica.set_value(old_value)

            if self.backjump is None:
                continue

            if self.backjump.target_node != node_index:
                # executing backjumping
                return scenario, False

            self.notify_observers_backjump_end(self.backjump, pattern)

            pattern_to_remove = self.backjump_get_pattern_to_remove(self.backjump)
            #removed = self.remove_matches_from_pattern(matches, matches_tree, pattern_to_remove)
            #print("matches removed: " + str(removed))

            self.backjump = None
            #backjumping complete

        entry_replica.set_is_valid(False)
        entry_replica.set_value(old_value)

        #packing backjumping
        assert(self.backjump is None)
        #self.backjump = self.get_backjump_info(entry_replica, pattern, replica)
        #self.backjump = None

        if self.backjump is not None:
            self.notify_observers_backjump_req(self.backjump)

        #backtracking
        return scenario, False

    def remove_matches_from_pattern(self, matches, matches_tree, pattern_to_remove):
        matcher = BartezDictionaryTrieNodeVisitorMatchPattern(pattern_to_remove)
        matches_tree.get_root().accept(matcher)
        matches_to_remove = matcher.detach_matches()

        for m in matches_to_remove:
            if m not in matches:
                continue

            matches.remove(m)

        return len(matches_to_remove)

    def get_failing_pattern(self, entry, scenario, failing_related_entry):
        r_entries = entry.get_relations_entries(scenario.entries)
        if failing_related_entry in r_entries is False:
            return None

        entry_value = entry.get_value()
        r_entries_index = [e.absolute_index() for e in r_entries]
        relation_pos = r_entries_index.index(failing_related_entry.absolute_index())
        failing_pattern_list = list('.' * entry.get_length())
        failing_pattern_list[relation_pos] = entry_value[relation_pos]
        failing_pattern = "".join(failing_pattern_list)
        return failing_pattern

    def get_backjump_info(self, entry, pattern, scenario):
        #        if pattern.count('.') != 0 and self.__matcher.has_match(pattern):
        # pattern has matches, no need to backjump?
        #            return None

        if pattern.count('.') == 0:
            return None

        source_node = entry.absolute_index()
        target_node = -1

        r_entries = entry.get_relations()
        r_entries_index = [e.get_index() for e in r_entries]

        for path_index in reversed(scenario.path):
            entry_in_path = scenario.entries[path_index]
            entry_in_path_index = entry_in_path.absolute_index()
            if entry_in_path_index in r_entries_index:
                relation_index = r_entries_index.index(entry_in_path_index)
                relation = r_entries[relation_index]
                relation_entry = scenario.entries[relation.get_index()]
                pos_in_entry, pos_in_other = get_entries_intersection(relation.get_coordinate(), entry, relation_entry)
                relation_value = relation_entry.get_value()
                new_pattern_list = list('.'*len(relation_value))
                new_pattern_list[pos_in_other] = pattern[pos_in_entry]
                target_node = -1

                new_pattern = "".join(new_pattern_list)
                if new_pattern == '.'*len(new_pattern):
                    continue

                target_node = relation_entry.absolute_index()

                if self.__matcher.has_match(new_pattern) is True:
                     break

        if target_node == -1:
            return None

        #target_node = scenario.path[scenario.path.index(target_node)]

        return BartezBackJump(source_node, target_node, pattern, scenario.path, scenario)

    def get_backjump_info2(self, entry, pattern, scenario):
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

                if pattern == new_pattern:
                    continue

                if self.__matcher.has_match(new_pattern) is True:
                    break

        bj = 0 if backjump_to_index == 0 else scenario.entries[backjump_to_index].absolute_index()
        return BartezBackJump(entry.absolute_index(), bj, pattern, scenario.path, scenario)

    def backjump_get_pattern_to_remove(self, backjump):
        new_pattern = backjump.scenario.entries[backjump.target_node].get_pattern(backjump.scenario.entries)

        entry = backjump.scenario.entries[backjump.source_node]
        related_entry = backjump.scenario.entries[backjump.target_node]
        failing_pattern = self.get_failing_pattern(related_entry, backjump.scenario, entry)
        related_pattern = related_entry.get_pattern(backjump.scenario.entries)
        entry_pattern = entry.get_pattern(backjump.scenario.entries)

        r_entries = related_entry.get_relations_entries(backjump.scenario.entries)
        r_entries_index = [e.absolute_index() for e in r_entries]
        relation_pos = r_entries_index.index(entry.absolute_index())
        pattern_to_remove_list = list(new_pattern)

        for rpos in range(len(failing_pattern)):
            if failing_pattern[rpos] == '.':
                continue

            pattern_to_remove_list[rpos] = failing_pattern[rpos]

        #pattern_to_remove_list[relation_pos] = failing_pattern[relation_pos]
        pattern_to_remove = "".join(pattern_to_remove_list)

        if pattern_to_remove.count('.') == len(pattern_to_remove):
            return ""

        print("removing pattern: " + pattern_to_remove)
        return pattern_to_remove


    def forward_check(self, entry, scenario):
        r_entries = entry.get_relations_entries(scenario.entries)

        for r in r_entries:
            if r.is_valid() is True:
                continue

            r_pattern = r.get_pattern(scenario.entries)

            if self.__matcher.has_match(r_pattern) is False:
                return r, r_pattern, False

        return None, None, True

    def forward_check2(self, entry, scenario):
        return self.forward_check_do(entry, scenario, 0, 1)


    def forward_check_do(self, entry, scenario, depth, max_depth):
        if depth >= max_depth:
            return None, None, True

#        if scenario.forbidden.contains_pattern(entry.absolute_index(), entry.get_pattern(scenario.entries)) is True:
#            return None, None, False

        r_entries = entry.get_relations_entries(scenario.entries)

        for r in r_entries:
            if r.is_valid() is True:
                continue

            r_index = r.absolute_index()

            r_pattern = r.get_pattern(scenario.entries)
#            if scenario.forbidden.contains_pattern(r_index, r_pattern) is True:
#                return None, None, False

            if self.__matcher.has_match(r_pattern) is False:
                #scenario.forbidden.add_pattern(r_index, r_pattern)
                return r, r_pattern, False

        for r in r_entries:
            if self.forward_check_do(r, scenario, depth + 1, max_depth) is False:
                return None, None, False

        return None, None, True

    def notify_observers_backjump_end(self, backjump, pattern):
        # message = ( "\n from node " + str(backjump.source_node) +
        #             " [" + backjump.scenario.entries[backjump.source_node].description() + "]" +
        #             " to node " + str(backjump.target_node) + " [" +
        #             backjump.scenario.entries[backjump.target_node].description() + "]" +
        #             " with pattern: " + pattern)
        # message += ("\n backjumping from path: " + str(backjump.from_path) +
        #             "\n with old pattern: " + backjump.pattern)
        #
        # new_pattern = backjump.scenario.entries[backjump.target_node].get_pattern(backjump.scenario.entries)
        # message += "\n new pattern: " + new_pattern

        message = ( "\n from node " + str(backjump.source_node) +
                    " [" + backjump.scenario.entries[backjump.source_node].description() + "]" +
                    " to node " + str(backjump.target_node) +
                    " [" + backjump.scenario.entries[backjump.target_node].description() + "]")
        message += ("\n backjumping from path: " + str(backjump.from_path) +
                    "\n with old pattern: " + backjump.pattern)

        new_pattern = backjump.scenario.entries[backjump.target_node].get_pattern(backjump.scenario.entries)
        message += "\n with new pattern: " + new_pattern

        #pattern_to_remove = self.backjump_get_pattern_to_remove(backjump)
        #message += "\n pattern_to_remove: " + pattern_to_remove

        self.notify_observers_message("backjump end " + message)
        return

    def notify_observers_backjump_req(self, backjump):
        message = ( "\n from node " + str(backjump.source_node) +
                    " [" + backjump.scenario.entries[backjump.source_node].description() + "]" +
                    " to node " + str(backjump.target_node) +
                    " [" + backjump.scenario.entries[backjump.target_node].description() + "]")
        message += ("\n backjumping from path: " + str(backjump.from_path) +
                    "\n with old pattern: " + backjump.pattern)

        new_pattern = backjump.scenario.entries[backjump.target_node].get_pattern(backjump.scenario.entries)
        message += "\n with new pattern: " + new_pattern

        #entry = backjump.scenario.entries[backjump.source_node]
        #related_entry = backjump.scenario.entries[backjump.target_node]
        #failing_pattern = self.get_failing_pattern(entry, backjump.scenario, related_entry)
        #message += "\nwith failing pattern: " + failing_pattern

        self.notify_observers_message("backjump start " + message)
        return
