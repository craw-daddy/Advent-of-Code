from heapq import heappush, heappop

import math
import copy

DIRECTIONS = ['E', 'S', 'W', 'N']

def DijkstraGrid(grid, start='S', target=None, 
                 empty_space='.', facing='E', 
                 move_cost=1, turn_cost=0):
    '''A method to find shortest paths in a 2-dimensional grid.
       grid - the 2-dimensional grid
       start - the starting location as a (row, column) tuple or 'S', signifying that
               the starting location is denoted in the grid by the letter 'S', so we
               will find that starting location
       target - could be a list of tuples, a single tuple, None (to return the 
                full array of shortest distances), or 'E' to denote the target location
                in the grid (in which case we will search for it).  If the target is
                denoted by 'E', we assume that there is only one in the grid, otherwise
                the results will find one of the targets and use that.  
       facing - whether or not facing is important, denoted by a starting facing given
                as a cardinal direction (N, E, S, W), arbitrarily started as 'E'
       move_cost - assumed to be 1, but could be a fixed number, or (possibly) even a
                   function to return the cost (this functionality yet to be implemented)
       turn_cost - whether it costs to make a turn, assumed to be zero, this will be a cost
                   to make a turn by 90 degrees, so a 180 turn would be twice this amount
                   If this is a negative number, then results are unpredictable as you 
                   can then end up with a "cycle" that has a negative cost.  

       Note:  If the target is denoted by an 'E' in the grid, but is given as a tuple in 
       the input to the function, this method won't succeed, as then the 'E' won't be 
       interpreted as an "empty space".  
    '''
    if (not isinstance(facing, str)) or (facing not in DIRECTIONS):
        raise ValueError("facing must be one of ['E', 'S', 'W', 'N']")
    if not isinstance(start, tuple) and (isinstance(start, str) and (start != 'S')):
        raise ValueError("start must be either a 2-dimensional tuple, or 'S' in a single place in the grid") 

    #  We will make a copy of the grid, as we might be altering it (by changing
    #  a label of a starting or ending location) in this method
    grid = copy.deepcopy(grid)

    rows = len(grid)
    cols = len(grid[0])

    #  Find the starting location, if necessary
    if start == 'S':
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 'S':
                    grid[r][c] = empty_space
                    start = (r,c)

    #  Find the target location, if necessary
    if target == 'E':
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 'E':
                    grid[r][c] = empty_space
                    target = (r, c)
                    
    #  Set up an array of the turning costs from one direction to another, so
    #  that we can use it in the computations below.
    cost_of_turning = { (d,d): 0 for d in DIRECTIONS }
    cost_of_turning[('E','S')] = cost_of_turning[('E','N')] = turn_cost
    cost_of_turning[('S','E')] = cost_of_turning[('S','W')] = turn_cost
    cost_of_turning[('W','S')] = cost_of_turning[('W','N')] = turn_cost
    cost_of_turning[('N','E')] = cost_of_turning[('N','W')] = turn_cost
    cost_of_turning[('E','W')] = cost_of_turning[('W','E')] = 2*turn_cost
    cost_of_turning[('N','S')] = cost_of_turning[('S','N')] = 2*turn_cost
                    
    #  Initialize the distances to infinity, and the distance to the start as 0
    #  Note, need to keep track of the distance to get to a location from 
    #  the start, as well as the (current) facing of the mover when it arrives 
    #  at that location to account for the "turning cost" (if any).
    #  We keep track of the parent of a node as well, i.e. a node that we use
    #  to reach a node.
    distances = { (i,j): (math.inf, facing, None) for i in range(rows) for j in range(cols) }
    distances[start] = (0, facing, None)
    heap = [(0, start)]

    #  Perform the BFS from the start
    while heap:
        v = heappop(heap)
        current_distance = distances[v[1]][0]
        current_facing = distances[v[1]][1]
        for new_facing, (dx, dy) in zip(DIRECTIONS, [(0,1), (1, 0), (0,-1), (-1,0)]):
            nbr = (v[1][0] + dx, v[1][1] + dy)
            #  Check that the neighbor exists (i.e. we haven't gone off the grid)
            #  AND that the neighbor is actually empty
            if (0 <= nbr[0] < rows) and (0 <= nbr[1] < cols) and grid[nbr[0]][nbr[1]] == empty_space:
                new_distance = current_distance + move_cost + cost_of_turning[(current_facing, new_facing)]
                if new_distance < distances[nbr][0]:
                    heappush(heap, (new_distance, nbr))
                    distances[nbr] = (new_distance, new_facing, v[1])
        
    #  Return the information of interest, depending upon what the value of target is
    if target is not None:
        if isinstance(target, tuple):
            return distances[target][0]
        if isinstance(target, list):
            return { k: v[0] for k,v in distances.items() if k in target }
    else:
        return { k: v[0] for k,v in distances.items() }
