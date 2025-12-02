from container_ship import ContainerShip, MAX_COLS

#this will take in a containership object as input and returns a float representing the estimated cost to move toward a balanced ship.
#will also calculate the minimal crane move cost needed to transfer one top container to the lighter side, returms 0 if the ship is already balanced.
def balance_heuristic(ship: ContainerShip) -> float:
    # heuristic is 0 if already perfectly balanced — use a cheap check here.
    # Avoid calling `ship.is_goal()` because that may trigger a costly
    # `compute_min_possible_imbalance()` BFS; the heuristic is called
    # many times during A* and must be fast.
    if ship.get_balance_difference() == 0:
        return 0.0
    
    heavy_is_port = ship.port_weight > ship.starboard_weight
    left_half = MAX_COLS // 2 

    #these determine which columns are the heavier side
    heavy_cols = range(0, left_half) if heavy_is_port else range(left_half, MAX_COLS)
    light_cols = range(left_half, MAX_COLS) if heavy_is_port else range(0, left_half)

    #stores the lowest move cost found moving a container from heavy to light side
    #Considers both crane moves and horizontal slides
    min_cost = float('inf')
    found = False

    #sc = start column
    for sc in heavy_cols:
        start_pos, w = ship.get_top_container(sc)
        if not start_pos:
            continue
        
        # Check horizontal slides first (since thier cheaper)
        r_idx = start_pos[0] - 1
        c_idx = start_pos[1] - 1
        if ship.is_exposed(r_idx, c_idx):
            slides = ship.get_horizontal_slides_from_cell(r_idx, c_idx)
            for slide_start, slide_end, slide_weight in slides:
                # Check if slide moves container to light side
                slide_end_col = slide_end[1] - 1
                if slide_end_col in light_cols:
                    slide_cost = abs(slide_start[1] - slide_end[1])  # horizontal distance
                    if slide_cost < min_cost:
                        min_cost = slide_cost
                        found = True
        
        # Also check crane moves to light side
        for ec in light_cols:
            end_pos = ship.get_next_empty(ec)
            if not end_pos:
                continue

            cost = ship.calculate_move_cost(start_pos, end_pos)

            if cost < min_cost:
                min_cost = cost
                found = True
    #return large number so astar knows its expensive  
    return min_cost if found else 999999