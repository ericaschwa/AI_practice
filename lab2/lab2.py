# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    paths  = [[start]]
    while len(paths) > 0 and paths[-1][-1] != goal:
        path      = paths.pop()
        new_paths = []
        for node in graph.get_connected_nodes(path[-1]):
            if node not in path:
                new_paths[:0] = [path + [node]]
        paths   = new_paths + paths
    if len(paths) > 0 and paths[-1][-1] == goal:
        return paths[-1]
    else:
        return []

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    paths = [[start]]
    while len(paths) > 0 and paths[-1][-1] != goal:
        path      = paths.pop()
        new_paths = []
        for node in graph.get_connected_nodes(path[-1]):
            if node not in path:
                new_paths.append(path + [node])
        paths += new_paths
    if paths[-1][-1] == goal:
        return paths[-1]
    else:
        return []

## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    paths = [[start]]
    while len(paths) > 0 and paths[-1][-1] != goal:
        path      = paths.pop()
        new_paths = []
        for node in graph.get_connected_nodes(path[-1]):
            if node not in path:
                new_paths.append(path + [node])
        paths += sorted(new_paths,
                        key=lambda p: graph.get_heuristic(p[-1], goal)*-1)
    if paths[-1][-1] == goal:
        return paths[-1]
    else:
        return []

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    paths  = [[start]]
    path_levels = {1: [[start]]}
    while len(paths) > 0 and paths[-1][-1] != goal:
        path      = paths.pop()
        new_paths = []
        for node in graph.get_connected_nodes(path[-1]):
            if node not in path:
                new_paths[:0] = [path + [node]]
                level = len(new_paths[0])
                if level not in path_levels:
                    path_levels[level] = []
                path_levels[level].append(new_paths[0])
                if len(path_levels[level]) > beam_width:
                    to_remove = max(path_levels[level],
                                    key=lambda p: graph.get_heuristic(p[-1], goal))
                    path_levels[level] = remove_from_l(path_levels[level], to_remove)
                    paths              = remove_from_l(paths,              to_remove)
                    new_paths          = remove_from_l(new_paths,          to_remove)
        paths = new_paths + paths
    if len(paths) > 0 and paths[-1][-1] == goal:
        return paths[-1]
    else:
        return []

# Returns given list without given item, assuming no repeat appearances
def remove_from_l(l, item):
    try:
        i = l.index(item)
        return l[:i] + l[i+1:]
    except:
        return l

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    result = 0
    for i in xrange(1, len(node_names)):
        result += graph.get_edge(node_names[i-1], node_names[i]).length
    return result

def branch_and_bound(graph, start, goal):
    if start == goal: return [start]
    paths  = [[start]]
    while len(paths) > 0:
        path      = min(paths, key=lambda p: path_length(graph, p))
        paths.remove(path)
        new_paths = []
        for node in graph.get_connected_nodes(path[-1]):
            if node == goal:
                return path + [node]
            if node not in path:
                new_paths.append(path + [node])
        paths   = new_paths + paths
    return []

def a_star(graph, start, goal):
    if start == goal: return [start]
    paths    = [[start]]
    extended = set()
    while len(paths) > 0:
        path = min(paths,
                   key=lambda p: path_length(graph, p) + \
                                 graph.get_heuristic(p[-1], goal))
        paths.remove(path)
        if path[-1] in extended: continue
        extended.add(path[-1])
        new_paths = []
        for node in graph.get_connected_nodes(path[-1]):
            if node == goal:
                return path + [node]
            if node not in path:
                new_paths.append(path + [node])
        paths   = new_paths + paths
    return []

## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    for n in graph.nodes:
        real_dist = path_length(graph, branch_and_bound(graph, n, goal))
        if real_dist < graph.get_heuristic(n, goal):
            return False
    return True

def is_consistent(graph, goal):
    for e in graph.edges:
        dist1 = graph.get_heuristic(e.node1, goal)
        dist2 = graph.get_heuristic(e.node2, goal)
        if e.length < abs(dist1 - dist2): return False
    return True

HOW_MANY_HOURS_THIS_PSET_TOOK = '4'
WHAT_I_FOUND_INTERESTING = 'Writing the search functions.'
WHAT_I_FOUND_BORING = 'Answering these questions.'
