import re


def get_entries_intersection(c, entry, other):
    pos_in_entry = c.x() - entry.x() if entry.vertical() else c.y() - entry.y()
    pos_in_other = c.x() - other.x() if other.vertical() else c.y() - other.y()
    return pos_in_entry, pos_in_other


def get_entries_by_traversal(entries, traversal):
    return list([entries[x] for x in traversal])


def get_pattern(entry_index, entries):
    entry = entries[entry_index]
    pattern = entry.value()
    pattern_as_list = list(pattern)
    #print entry.description(), ":"
    #print "  x: ", entry.x(), ", y: ", entry.y()

    for relation_index, relation in enumerate(entry.relations()):
        other_index = relation.index()
        other = entries[other_index]
        other_pattern = other.value()
        other_pattern_as_list = list(other_pattern)
        #print "  relation with ", other.description(), ":"
        pos_in_entry, pos_in_other = get_entries_intersection(relation.coordinate(), entry, other)
        char_other = other_pattern_as_list[pos_in_other]
        pattern_as_list[pos_in_entry] = char_other

    pattern_as_string = "".join(pattern_as_list)
    return pattern_as_string


def get_matches(dictionary, pattern, used_words):
    potential_matches = []
    page = dictionary.get_page(len(pattern) - 1)

    for dictionary_entry in page:
        word = dictionary_entry.get()
        if re.match(pattern, word) is not None:
            potential_matches.append(word)

    matches = (x for x in potential_matches if x not in used_words)
    return matches


def bridges(G):
  """
  Bridge detection algorithm based on WGB-DFS.
  """
  import networkx as nx
  from collections import defaultdict

  if G.is_directed():
    raise nx.NetworkXError('This function is for undirected graphs.\n'
                           'Use directed_wgb_dfs() for directed graphs.')

  class WhiteGrayBlackDFS:
    def __init__(self, G):
      # white: empty
      # gray: 1
      # black: 2

      self.visited = set()
      self.dfs_num = {}
      self.num = 0
      self.G = G
      self.back_edges = defaultdict(set)

    def bridges(self, parent, current):
      #print '{'
      #print 'parent, current:', parent, current
      #print 'dfs_num:', self.dfs_num
      self.visited.add(current)
      current_lowpoint = self.dfs_num[current] = self.num

      self.num += 1
      #print 'dfs_num:', self.dfs_num

      for child in G.neighbors(current):
        if child != parent:
          #print 'current, child:', current, child
          if not current in self.back_edges or (current in self.back_edges and not child in self.back_edges[current]):
            if child in self.visited:
              current_lowpoint = min(current_lowpoint, self.dfs_num[child])
            else:
              for x in self.bridges(current, child):
                yield x
              if self.child_lowpoint > self.dfs_num[current]:
                #print '>>> bridge:', current, child
                yield (current, child)
              current_lowpoint = min(current_lowpoint, self.child_lowpoint)

      #print 'parent, current, current_lowpoint:', parent, current, current_lowpoint
      #print 'dfs_num:', self.dfs_num
      #print '}'
      self.child_lowpoint = current_lowpoint

  dfs = WhiteGrayBlackDFS(G)

  for x in G:
    if not x in dfs.visited:
      #print x
      for e in dfs.bridges(x, x):
        yield e
