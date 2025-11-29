import heapq
from collections import namedtuple
from typing import Tuple, Dict
from container_ship import ContainerShip
from heuristic import balance_heuristic

#defines a container for each node in the Astar search tree
PathNode = namedtuple('PathNode', ['ship_state', 'g_cost', 'move_history'])

#will find minimal total crane time to reach goal balance Returns (move_history_list, total_g_cost) or (None, 0) if not found.
def a_star_search(intial_ship: ContainerShip, max_expansions: int = 100000):
    start_grid = intial_ship.grid_tuple()
    #heuristic estimate of cost from start to goal
    start_h = balance_heuristic(intial_ship)
    start_node = PathNode(intial_ship, 0, [])

    #priority queue (a min heap) stores (f_cost, counter, node)
    pq = []
    counter = 0
    heapq.heappush(pq,(start_h, counter, start_node))
    counter +=1

    # a dictionary to track the lowest cost to reach each grid state so no revisting worse paths 
    visited_costs: Dict[Tuple, float] = {start_grid: 0.0}
    expansions = 0

    #this is the main a star loop until the queue is empty or goal is found
    while pq:
        #pop the node with the lowest estimated total cost 
        f_cost, _, node = heapq.heappop(pq)
        ship = node.ship_state
        #gcost is the actual crane move cost to reach a state
        g_cost = node.g_cost

        if ship.is_goal():
            return node.move_history, g_cost
        
        expansions += 1
        if expansions > max_expansions:
            return None, 0
        
        for new_ship, move in ship.get_valid_moves():
            #total cost to reach new node
            new_g = g_cost + move.cost
            new_grid = new_ship.grid_tuple()
            if new_grid in visited_costs and new_g >= visited_costs[new_grid]:
                continue
            
            #saves the best cost to reach this state
            visited_costs[new_grid] = new_g
            #compute new hueristic cost for new ship
            h = balance_heuristic(new_ship)
            new_f = new_g + h

            #append the moves to the history-> put into new state into a PathNode-> push it into the queue with the fcost-> increment counter 
            new_history = node.move_history + [move]
            new_node = PathNode(new_ship,new_g,new_history)
            heapq.heappush(pq,(new_f,counter,new_node))
            counter += 1

    return None,0






