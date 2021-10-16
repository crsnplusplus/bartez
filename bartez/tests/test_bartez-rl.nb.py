#!/usr/bin/env python
# coding: utf-8

# In[8]:


import numpy as np
from tensorforce.environments import Environment
import networkx as nx

from bartez.graph.graph import BartezGraph
import bartez.tests.test_utils as test_utils
from bartez.crossword import Crossworld
from bartez.symbols import SquareValues
import bartez.tests.test_utils as test_utils

import copy


# In[9]:


class CrosswordModel(object):
    def __init__(self):
        self.__crossword = test_utils.get_test_crossword3x3()
        self.__crossword_start = None
        self.__valid_letters = list(map(chr, range(ord('a'), ord('z')+1)))
        self.__square_action_vec = list(self.__valid_letters) + list(SquareValues.char)
        self.__dictionary = test_utils.get_test_dictionary()
        self.__trie = test_utils.get_test_trie()
    
    def get_rows_count(self):
        return self.__crossword.get_rows_count()

    def get_columns_count(self):
        return self.__crossword.get_columns_count()
    
    def get_squares_count(self):
        return self.get_rows_count() * self.get_columns_count()
    
    def get_actions_per_square_count(self):
        return len(self.__square_action_vec)
    
    #def get_actions_count(self):
    #    return self.get_squares_count() * len(self.__square_action_vec)
    
    def print_info(self):
        self.__crossword.print_crossword()
        print("rows: " + str(self.get_rows_count()))
        print("columns: " + str(self.get_columns_count()))
    
    def reset(self):
        #distribution = np.random.randint(2, size=self.get_squares_count())
        distribution = np.array([0, 0, 1, 0, 1, 1, 1, 1, 1])
        #print(type(distribution))
        print(distribution)
        cols = self.get_columns_count()
        for i in range(len(distribution)):
            row = int(i / cols)
            col = int(i % cols)
            value = SquareValues.char if (distribution[i] == 0) else SquareValues.block
            #print("i     : " + str(i))
            #print("row   : " + str(row))
            #print("col   : " + str(col))
            #print("rows  : " + str(self.get_columns_count()))
            #print("cols  : " + str(cols))
            #print("distribution[i]: " + str(distribution[i]))
            #print("value : " + str(value))
            self.__crossword.set_symbol(row, col, value)
        self.__crossword.prepare()
        self.__crossword_start = copy.copy(self.__crossword)
        self.print_info()
        
        entries = self.__crossword.get_entries()
        graph = test_utils.get_test_graph(self.__crossword)
        #nx.draw(graph, with_labels = True)
        print(type(graph))
        print(type(entries))
        print("\n".join([(e.get_description() + " [" +
                         str(e.get_coordinate_x()) + " " +
                         str(e.get_coordinate_y()) + "] ") for e  in entries]))

    
    def crossword_to_state(self, crossword):
        
        pass
    
    def perform_action(self, action):
        reward = 0
        cols = self.get_columns_count()
        actions_per_square_count = self.get_actions_per_square_count()
        modulo = action % actions_per_square_count
        
        letter = action / actions_per_square_count
        row = modulo / cols
        col = modulo % cols
        
        self.set_value(row, col, letter)
        return reward


# In[10]:


class CrosswordEnvironment(Environment):
    def __init__(self):
        super().__init__()
        self.__model = CrosswordModel()
        self.NUM_ACTIONS = self.__model.get_actions_count()
        self.NUM_STATES = self.__model.get_squares_count()
        print("States: " + str(self.NUM_STATES))
        print("Actions: " + str(self.NUM_ACTIONS))
        print("Actions per square: " + str(self.__model.get_actions_per_square_count()))
        
    def states(self):
        return dict(type='int', num_values=self.NUM_STATES)
    
    def actions(self):
        return dict(type=int, shape=(), num_values=self.NUM_ACTIONS)
    
    def reset(self):
        # Initial state and associated action mask
        return self.__model.reset()
    
    def execute(self, action):
        reward = self.__model.perform_action(action)
        
        return next_state, false, reward


# In[11]:


def start():
    env = CrosswordEnvironment()
    env.reset()


# In[12]:


start()


# In[ ]:





# In[ ]:




