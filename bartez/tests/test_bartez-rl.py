#!/usr/bin/env python
# coding: utf-8

import numpy as np
import networkx as nx
from tensorforce.environments import Environment
from tensorforce.agents import Agent
from tensorforce.execution import Runner
from collections import namedtuple

from bartez.graph.graph import BartezGraph
from bartez.crossword import Crossworld
from bartez.symbols import SquareValues, Symbols, symbols_to_base0, base0_to_symbols
from bartez.dictionary.trie import BartezDictionaryTrie
from bartez.dictionary.trie_pattern import BartezDictionaryTriePatternMatcher
import bartez.tests.test_utils as test_utils

from copy import copy

# Symbols.FIRST + 0 = ?, first action
ActionListTuple = namedtuple('Symbols', ['FIRST_ACTION', 'LAST_ACTION', 'OFFSET'])
ActionList = ActionListTuple(ord(Symbols.FIRST), ord(Symbols.LAST), 0) 


class CrosswordModel(object):
    def __init__(self):
        self.__crossword = Crossworld(4, 4)
        #self.__crossword = test_utils.get_test_crossword3x3()
        #self.__crossword = test_utils.get_test_crossword()
        self.__actions = range(ActionList.FIRST_ACTION, ActionList.LAST_ACTION)
        #self.__dictionary = test_utils.get_test_dictionary()
        self.__trie = test_utils.get_test_trie()
        self.__matcher = BartezDictionaryTriePatternMatcher()
        self.__matcher.load_from_dictionary_trie(self.__trie)
    

    def get_rows_count(self):
        return self.__crossword.get_rows_count()


    def get_columns_count(self):
        return self.__crossword.get_columns_count()
    

    def get_squares_count(self):
        return self.get_rows_count() * self.get_columns_count()
    

    def get_actions_per_square_count(self):
        return len(self.__actions)
    

    def get_actions_count(self):
        return len(self.__actions) * self.get_squares_count()
    
    
    def get_action_space(self):
        d = dict( actions=dict(type='int', num_values=self.get_actions_per_square_count(), shape=(self.get_squares_count())) )
        return d


    def get_squares_pos_with_no_char_neighbours(self):
        return self.__crossword.get_squares_pos_with_no_char_neighbours()


    def get_state_space(self):
        return dict ( states=dict(type='int', num_values=self.get_actions_per_square_count(), shape=(self.get_squares_count(),)) )


    def reset(self):
        squares_count = self.get_squares_count()
        blocks_count = int(squares_count * (np.random.sample(1) * 0.4 + 0.2))
        char_count = squares_count - blocks_count
        char_symbol = SquareValues.char
        block_symbol = SquareValues.block
        distribution = np.array([char_symbol] * char_count + [block_symbol] * blocks_count)
        np.random.shuffle(distribution)
        
        print(distribution)
        cols = self.get_columns_count()
        for i in range(len(distribution)):
            row = int(i / cols)
            col = int(i % cols)
            symbol = distribution[i]
            self.__crossword.set_symbol(row, col, symbol)
        self.__crossword.print_crossword()
        self.__crossword.prepare()

        if self.__crossword.has_squares_with_no_char_neighbours():
            squares = self.__crossword.get_squares_pos_with_no_char_neighbours()
            self.__crossword.set_blocks(squares)
            self.__crossword.prepare()
            self.__crossword.print_crossword()
            assert(self.__crossword.has_squares_with_no_char_neighbours() == False)
        
        entries = self.__crossword.get_entries()
#        print("Entries (" + str(len(entries)) + ")" )
#        print("\n".join([(e.get_description() + " [" +
#                         str(e.get_coordinate_x()) + " " +
#                         str(e.get_coordinate_y()) + "] ") for e  in entries]))

        if len(entries)  < 2:
            print("Not enough nodes (< 2), retrying")
            return self.reset()

        graph = test_utils.get_test_graph(self.__crossword)
        if nx.is_connected(graph) == False:
            print("Not connected, retrying")
            return self.reset()

        return self.get_states()


    def get_states(self):
        grid_states = np.zeros(self.get_squares_count())
        cols = self.get_columns_count()
        for r in range(0, self.get_rows_count()):
            for c in range(0, cols):
                symbol = self.__crossword.get_value(r, c)
                idx = r * cols + c
                grid_states[idx] = ord(symbol) - ActionList.FIRST_ACTION
        #return grid_states
        #return dict ( states=dict(type='int', num_values=self.get_actions_per_square_count(), shape=(self.get_squares_count(),)) )
        d = dict ( states=grid_states )
        return d
        

    def apply_get_reward(self, row, col, char):
        reward = 0
        
        value = self.__crossword.get_value(row, col)
        if char == SquareValues.block and value == SquareValues.block:
            reward += 0.01
        elif char == SquareValues.block:
            return -1
        elif value == SquareValues.block:
            return -1
        
        self.__crossword.set_symbol(row, col, char)

        entries = self.__crossword.get_entries()
        # rewards
#        single_word_reward = 1 / len(entries)
        good_word_reward = 0.2
        blank_reward = -0.2
        bad_pattern_reward = -0.1
        good_pattern_reward = 0.1
        
        total_blank_count = 0
        
        for _, e in enumerate(entries):
            pattern = e.get_value()
            blank_count = pattern.count(SquareValues.char)
            total_blank_count += blank_count
            matches = self.__matcher.get_matches(pattern)
            matches_count = len(matches)

            entry_reward = 0
            if matches_count == 1 and blank_count == 0:
                entry_reward += good_word_reward
            
            if matches_count == 0:
                #entry_reward += bad_pattern_reward * (len(pattern) - blank_count)
                entry_reward += bad_pattern_reward
            else:
                #entry_reward += good_pattern_reward * (len(pattern) - blank_count)
                entry_reward += good_pattern_reward

            reward += entry_reward
            reward += blank_count * blank_reward

        return reward


    def is_terminal(self):
        entries = self.__crossword.get_entries()
        for _, e in enumerate(entries):
            pattern = e.get_value()
            blank_count = pattern.count(SquareValues.char)
            matches = self.__matcher.get_matches(pattern)
            if blank_count == 0 and len(matches) == 1:
                continue
            else:
                return False
        return True


    def perform_actions(self, actions):
        #row, col, char = self.unpack_action(action)
        reward = 0
        action_index = 0
        for r in range(0, self.get_rows_count()):
            for c in range(0, self.get_columns_count()):
                action = chr ( actions['actions'][action_index] + ActionList.FIRST_ACTION )
                reward += self.apply_get_reward(r, c, action)
                action_index = action_index + 1
        return reward


    def print_info(self):
        self.__crossword.print_crossword()
        print("rows: " + str(self.get_rows_count()))
        print("columns: " + str(self.get_columns_count()))


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
        

    def states(self):
        #num_values = self.__model.get_actions_per_square_count()
        #return dict ( states=dict(type='int', num_values=num_values, shape=(self.NUM_STATES,)) )
        return self.__model.get_state_space()


    def actions(self):
        #return dict(type='int', num_values=self.NUM_ACTIONS)
        #return dict ( states=dict(type='int', num_values=num_values, shape=(self.NUM_STATES,)) )
        return self.__model.get_action_space()


    def reset(self):
        #state = np.random.random(size=(self.NUM_STATES,))
        #states = dict (states=new_states)
        #return states
        return self.__model.reset()
    

    def execute(self, action):
        reward = self.__model.perform_actions(action)
        next_states = self.__model.get_states()
        is_terminal = self.__model.is_terminal()
        return next_states, is_terminal, reward

    
    def print_crossword(self):
        self.__model.print_info()



def start():
    environment = CrosswordEnvironment()
    episodes_count = 10000
    states = environment.reset()

    agent_adam = Agent.create(
        agent='tensorforce', environment=environment, update=64,
        optimizer=dict(optimizer='adam', learning_rate=1e-3),
        objective='policy_gradient', reward_estimation=dict(horizon=20)
    )

    agent_ppo = Agent.create(
        agent='ppo', environment=environment, batch_size=10, learning_rate=1e-3, max_episode_timesteps=episodes_count
    )

    agent = agent_adam

    # Train for episodes_count episodes
    max_count = 1000
    for _ in range(episodes_count):
        states = environment.reset()
        initial_states = copy(states)
        terminal = False
        count = 0
        while not terminal and count != max_count:
            actions = agent.act(states=states)
            states, terminal, reward = environment.execute(action=actions)
            agent.observe(terminal=terminal, reward=reward)
            count += 1
            environment.print_crossword()
            print("iteration: " + str(count))
            print("reward: " + str(reward))
            
    # Evaluate for episodes_count episodes
    sum_rewards = 0.0
    for _ in range(episodes_count):
        states = environment.reset()
        internals = agent.initial_internals()
        terminal = False
        while not terminal:
            actions, internals = agent.act(
                states=states, internals=internals,
                independent=True, deterministic=True
            )
            states, terminal, reward = environment.execute(actions=actions)
            sum_rewards += reward

    print('Mean episode reward:', sum_rewards / episodes_count)

    # Close agent and environment
    agent.close()
    environment.close()


start()
