from collections import deque

import math

def DijkstraGrid(grid, start, target=None, 
                 empty_space='.', facing='E', 
                 move_cost=1, turn_cost=0):
    '''A method to find shortest paths in a 2-dimensional grid.
       grid - the 2-dimensional grid
       start - the starting location as a (row, column) tuple
       target - could be a list of elements, a single tuple, or None (to return the 
                full array of shortest distances
       facing - whether or not facing is important, denoted by a starting facing given
                as a cardinal direction (N, E, S, W), arbitrarily started as 'E'
       move_cost - assumed to be 1, but could be a fixed number, or (possibly) even a
                   function to return the cost (this functionality yet to be implemented)
       turn_cost - whether it costs to make a turn, assumed to be zero, this will be a cost
                   to make a turn by 90 degrees, so a 180 turn would be twice this amount
    '''
    DIRECTIONS = ['E', 'S', 'W', 'N']
    if (not isinstance(facing, str)) or (facing not in DIRECTIONS):
        raise ValueError("facing must be one of ['E', 'S', 'W', 'N']")
    
    rows = len(grid)
    cols = len(grid[0])

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
    distances = { (i,j): (math.inf, facing) for i in range(rows) for j in range(cols) }
    distances[start] = (0, facing)
    queue = deque([start])

    #  Perform the BFS from the start
    while queue:
        v = queue.popleft()
        current_distance = distances[v][0]
        current_facing = distances[v][1]
        for new_facing, direction in zip(DIRECTIONS, [(0,1), (1, 0), (0,-1), (-1,0)]):
            nbr = (v[0] + direction[0], v[1] + direction[1])
            #  Check that the neighbor exists (i.e. we haven't gone off the grid)
            #  AND that the neighbor is actually empty
            if (0 <= nbr[0] < rows) and (0 <= nbr[1] < cols) and grid[nbr[0]][nbr[1]] == empty_space:
                new_distance = current_distance + move_cost + cost_of_turning[(current_facing, new_facing)]
                if new_distance < distances[nbr][0]:
                    queue.append(nbr)
                    distances[nbr] = (new_distance, new_facing)
    
    #  Return the information of interest, depending upon what the value of target is
    if target is not None:
        if isinstance(target, tuple):
            return distances[target][0]
        if isinstance(target, list):
            return { k: v[0] for k,v in distances.items() if k in target }
    else:
        return { k: v[0] for k,v in distances.items() }

