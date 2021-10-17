#!/usr/bin/env python
# coding: utf-8

from os import environ
import numpy as np
import networkx as nx
from tensorforce.environments import Environment
from tensorforce.agents import Agent
from tensorforce.agents import DoubleDQN
from tensorforce.execution import Runner
from collections import namedtuple
from random import randrange, random, randint

from bartez.graph.graph import BartezGraph
from bartez.crossword import Crossworld
from bartez.symbols import SquareValues, Symbols, symbols_to_base0, base0_to_symbols
from bartez.dictionary.trie import BartezDictionaryTrie
from bartez.dictionary.trie_pattern import BartezDictionaryTriePatternMatcher
from bartez.dictionary.trie_dust import DustDictionaryTriePatternMatcher, dust_trie_import_from_file
import bartez.tests.test_utils as test_utils

from copy import copy
from datetime import datetime

# Symbols.FIRST + 0 = ?, first action
ActionListTuple = namedtuple('Symbols', ['FIRST_ACTION', 'LAST_ACTION', 'OFFSET'])
ActionList = ActionListTuple(ord(Symbols.FIRST), ord(Symbols.LAST), 0) 


class CrosswordModel(object):
    def __init__(self):
        self.__crossword = Crossworld(4, 4)
        #self.__crossword = test_utils.get_test_crossword3x3()
        #self.__crossword = test_utils.get_test_crossword()
        #self.__dictionary = test_utils.get_test_dictionary()
        #self.__trie = test_utils.get_test_trie()
        #self.__trie = test_utils.get_test_trie_corriere_it()
        #self.__trie = test_utils.get_test_trie_nouns_it()
        #self.__matcher = BartezDictionaryTriePatternMatcher()
        #self.__matcher.load_from_dictionary_trie(self.__trie)
        self.__matcher = dust_trie_import_from_file(test_utils.get_test_dictionary_corriere_path())
        rows = self.get_rows_count()
        cols = self.get_columns_count()
        actions = self.get_actions_per_square_count()
        self.__actions = [ [r, c, a] for r in range(0, rows) for c in range(0, cols) for a in range(0, actions) ]


    def get_rows_count(self):
        return self.__crossword.get_rows_count()


    def get_columns_count(self):
        return self.__crossword.get_columns_count()
    

    def get_squares_count(self):
        return self.get_rows_count() * self.get_columns_count()
    

    def get_actions_per_square_count(self):
        return len(range(ActionList.FIRST_ACTION, ActionList.LAST_ACTION + 1))
    

    def get_actions_count(self):
        return len(self.__actions)
    

    def get_action_space(self):
        return {
            "r": dict(type="int", num_values=self.get_rows_count()),
            "c": dict(type="int", num_values=self.get_columns_count()),
            "symbol": dict(type="int", num_values=self.get_actions_per_square_count()),
        }

    def get_squares_pos_with_no_char_neighbours(self):
        return self.__crossword.get_squares_pos_with_no_char_neighbours()


    def get_state_space(self):
        return dict ( states=dict(type='int', num_values=self.get_actions_per_square_count(), shape=(self.get_squares_count(),)) )


    def get_value(self, r, c):
        return self.__crossword.get_value(r, c)


    def reset(self):
        squares_count = self.get_squares_count()
        #blocks_count = int(squares_count * (np.random.sample(1) * 0.3 + 0.1))
        blocks_count = 1
        char_count = squares_count - blocks_count
        char_symbol = SquareValues.char
        block_symbol = SquareValues.block
        #distribution = np.array([char_symbol] * char_count + [block_symbol] * blocks_count)
        #np.random.shuffle(distribution)
        distribution = np.array([char_symbol] * squares_count)
        distribution[5] = block_symbol
        #print(distribution)
        cols = self.get_columns_count()
        for i in range(len(distribution)):
            row = int(i / cols)
            col = int(i % cols)
            symbol = distribution[i]
            self.__crossword.set_symbol(row, col, symbol)
        #self.__crossword.print_crossword()
        self.__crossword.prepare()

        if self.__crossword.has_squares_with_no_char_neighbours():
            squares = self.__crossword.get_squares_pos_with_no_char_neighbours()
            self.__crossword.set_blocks(squares)
            self.__crossword.prepare()
            #self.__crossword.print_crossword()
            assert(self.__crossword.has_squares_with_no_char_neighbours() == False)
        
        entries = self.__crossword.get_entries()

        if len(entries)  < 2:
            #print("Not enough nodes (< 2), retrying")
            return self.reset()

        graph = test_utils.get_test_graph(self.__crossword)
        if nx.is_connected(graph) == False:
            #print("Not connected, retrying")
            return self.reset()

        if (random() > 1):
            entries_count = len(entries)
            random_entry = entries[randrange(entries_count)]
            random_words = self.__matcher.get_matches(random_entry.get_value())
            matches_count = len(random_words)
            random_word = random_words[randrange(matches_count)]
            random_word_len = len(random_word)
            random_word_list = list(random_word)
            random_word_list[randrange(random_word_len)] = SquareValues.char
            random_word = ''.join([str(elem) for elem in random_word_list])
            random_entry.set_value(random_word)
            self.__crossword.set_board_value_from_entry(random_entry)

        if (random() > 1):
            entries_count = len(entries)
            random_entry = entries[randrange(entries_count)]
            random_words = self.__matcher.get_matches(random_entry.get_value())
            matches_count = len(random_words)
            random_word = random_words[randrange(matches_count)]
            random_word_len = len(random_word)
            random_word_list = list(random_word)
            random_word_list[randrange(random_word_len)] = SquareValues.char
            random_word = ''.join([str(elem) for elem in random_word_list])
            #print("Random word: " + random_word)
            random_entry.set_value(random_word)
            
            self.__crossword.set_board_value_from_entry(random_entry)

        return self.get_states()


    def get_states(self):
        grid_states = np.zeros(self.get_squares_count())
        cols = self.get_columns_count()
        for r in range(0, self.get_rows_count()):
            for c in range(0, cols):
                symbol = self.__crossword.get_value(r, c)
                idx = r * cols + c
                grid_states[idx] = ord(symbol) - ActionList.FIRST_ACTION
        d = dict ( states=grid_states )
        return d
        

    def apply_and_get_reward(self, row, col, char):
        # rewards
        entry_good_reward = 0.4
        entry_partial_good_reward = 0.1
        #entry_bad_malus  = -0.04
        entry_bad_malus  = 0
        blank_malus      = -0.2
        total_blank_count = 0
        reward = 0
        
        value = self.__crossword.get_value(row, col)
        if (char == SquareValues.block or value == SquareValues.block or  char == value) == False:
            self.__crossword.set_symbol(row, col, char)
            self.__crossword.update_entries_from_board_value(row, col, char)
            #self.__crossword.print_info()
            #self.__crossword.print_crossword()
        
        entries = self.__crossword.get_entries()

        for e in entries:
            pattern = e.get_value()
            blank_count = pattern.count(SquareValues.char)
            matches = self.__matcher.get_matches(pattern)
            matches_count = len(matches)

            if matches_count == 1 and blank_count == 0:
                reward += entry_good_reward
                #print("Complete entry found [" + str(e.get_coordinate_x()) + ","
                #                               + str(e.get_coordinate_y()) + "] " + e.get_description() + " - " + e.get_value())
                #self.print_crossword()
            else:
                reward += entry_bad_malus

            reward += blank_count * blank_malus
            total_blank_count += blank_count

        return reward


    def is_terminal(self):
        entries = self.__crossword.get_entries()
        complete_entries = 0
        for e in entries:
            pattern = e.get_value()
            blank_count = pattern.count(SquareValues.char)
            if blank_count == 0:
                complete_entries = complete_entries + 1

        is_terminal = complete_entries == len(entries)
        if is_terminal:
            print("Completed")
            self.print_crossword()
        return is_terminal


    def perform_actions(self, action):
        r = action["r"]
        c = action["c"]
        symbol = chr(action["symbol"] + ActionList.FIRST_ACTION)
        reward = self.apply_and_get_reward(r, c, symbol)
        return reward


    def print_crossword(self):
        entries = self.__crossword.get_entries()
        self.__crossword.clear_all_non_blocks()
        self.__crossword.set_board_values_from_entries(entries, True)
        self.__crossword.print_info()
        self.__crossword.print_crossword()


#########################################
# CrosswordEnvironment
#########################################
class CrosswordEnvironment(Environment):
    def __init__(self):
        super().__init__()
        self.__model = CrosswordModel()
        self.NUM_ACTIONS = self.__model.get_actions_count()
        self.NUM_STATES = self.__model.get_squares_count()
        print("NUM_STATES : " + str(self.NUM_STATES))
        print("NUM_ACTIONS: " + str(self.NUM_ACTIONS))
        print("Actions per square: " + str(self.__model.get_actions_per_square_count()))
        

    def get_squares_count(self):
        return self.__model.get_squares_count()


    def get_actions_per_square_count(self):
        return self.__model.get_actions_per_square_count()


    def get_value(self, r, c):
        return self.__model.get_value(r, c)


    def states(self):
        return self.__model.get_state_space()


    def actions(self):
        return self.__model.get_action_space()


    def reset(self):
        return self.__model.reset()
    

    def execute(self, action):
        reward = self.__model.perform_actions(action)
        next_states = self.__model.get_states()
        is_terminal = self.__model.is_terminal()
        return next_states, is_terminal, reward

    
    def print_crossword(self):
        self.__model.print_crossword()


def start():
    environment = CrosswordEnvironment()
    
    episodes_count = 5000
    batch_size = environment.get_squares_count() * 5
    max_moves = batch_size
    total_count = 0
    total_iterations_count =  episodes_count * batch_size
    update_frequency = 1000
    highest_reward = -100

    agent_adam = Agent.create(
        agent='tensorforce', environment=environment, update=64, memory=10000,
        optimizer=dict(optimizer='adam', learning_rate=1e-3),
        objective='policy_gradient', reward_estimation=dict(horizon=20)
    )

    agent_ddqn = Agent.create(
        agent='ddqn',
        environment=environment,
        batch_size=batch_size,
        memory=1000000,
        horizon=1,
        exploration=0.3,
        learning_rate=1e-4,
        summarizer=dict(
            directory='./data/summaries',
            summaries=['all']
        ),
    )

    agent = agent_ddqn



    # Train for episodes_count episodes
    for episode in range(episodes_count):
        states = environment.reset()
        #print("********************************")
        #print("New board:")
        #print(" - episode: " + str(episode) + "/" + str(episodes_count))
        #environment.print_crossword()
        terminal = False
        moves = 0
        while not terminal and moves < max_moves:
            action = agent.act(states=states)
            r = action["r"]
            c = action["c"]
            value = environment.get_value(r, c)
            
            states, terminal, reward = environment.execute(action=action)
            agent.observe(terminal=terminal, reward=reward)

            symbol = chr(action["symbol"] + ActionList.FIRST_ACTION)

            if (value == SquareValues.block or symbol == SquareValues.block or value == symbol) == False:
                if value == SquareValues.block:
                    value = '#'
                elif value == SquareValues.char:
                    value = '.'

            #if total_count % update_frequency == 0 or reward > 0:
            if reward > highest_reward:
                highest_reward = reward
            if total_count % update_frequency == 0:
                print("################################")
                print("episode: " + str(episode) + "/" + str(episodes_count))
                print("iteration: " + str(total_count) + "/" + str(total_iterations_count))
                print("perform: ["+str(r) +"]["+str(c)+"] = " + str(value) + " -> " + symbol)
                print("highest reward: " + str(highest_reward))
                print("reward: " + str(reward))
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print("time =", current_time)

                environment.print_crossword()
                print("")
            total_count += 1
            moves += 1

    print("-------------")
    environment.print_crossword()

    print("Evaluation:")
    # Evaluate for episodes_count episodes
    sum_rewards = 0.0
    for _ in range(episodes_count):
        states = environment.reset()
        internals = agent.initial_internals()
        terminal = False
        moves = 0
        while not terminal and moves < max_moves:
            action, internals = agent.act(
                states=states, internals=internals,
                independent=True, deterministic=True
            )
            states, terminal, reward = environment.execute(action=action)
            sum_rewards += reward
            moves = moves + 1

    print('Mean episode reward:', sum_rewards / episodes_count)

    # Close agent and environment
    agent.close()
    environment.close()


def start2():
    crossword = Crossworld(5, 4)
    crossword.prepare()
    crossword.print_info()
    crossword.clear_all_non_blocks()
    crossword.print_crossword()

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'l', 'm', 'n', 'o', 'p' ]
    entries = crossword.get_entries()
    for e in entries:
        new_pattern = len(e.get_value()) * letters[e.absolute_index()]
        #crossword.set_value_from_entry(e)
        print("--------------------------------")
        crossword.clear_all_non_blocks()
        crossword.apply_entry_on_relations(e, new_pattern)
        
        crossword.set_board_values_from_entries(entries)
        crossword.print_info()
        crossword.print_crossword()
        continue

def start3():
    crossword = Crossworld(5, 4)
    crossword.prepare()
    crossword.print_info()
    crossword.clear_all_non_blocks()
    crossword.print_crossword()
    rows = crossword.get_rows_count()
    cols = crossword.get_columns_count()

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'k', 'j', 'i', 'l',
               'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'w', 'x', 'y', 'z']
    entries = crossword.get_entries()
    #for i in range(10):
        #r = randint(0, crossword.get_rows_count() - 1)
        #c = randint(0, crossword.get_columns_count() - 1)
        #letter = letters[randint(0, len(letters))]
    i = 0
    for r in range(rows):
        for c in range(cols):
            letter = letters[i]
            print("[" + str(r) + ", " + str(c) + "]" + " -> " + letter)
            crossword.set_symbol(r, c, letter)
            crossword.update_entries_from_board_value(r, c, letter)
        
            #crossword.set_board_values_from_entries(entries)
            crossword.print_info()
            crossword.print_crossword()
            i = i + 1
            continue

start()


