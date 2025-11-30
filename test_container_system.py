import os
from container_ship import ContainerShip
from astar import a_star_search
from heuristic import balance_heuristic

#helper function to print list of moves
def print_moves(moves):
    if not moves:
        print("No moves found.")
        return
    print("\n=== MOVE HISTORY ===")
    for i, m in enumerate(moves, 1):
        print(f"{i}. Move {m.container_weight} lbs "
              f"from {m.start_pos} -> {m.end_pos}  (cost={m.cost})")

def main():
    # ------------------------------------------------------------
    # 1. LOAD MANIFEST
    # ------------------------------------------------------------

    #Place the path to the test manifest file here
    manifest_path = "manifests/testManifest.txt" 
    if not os.path.exists(manifest_path):
        print(f"ERROR: Manifest file not found: {manifest_path}")
        return

    print("Loading ship from manifest...")
    #create container ship object 
    ship = ContainerShip(manifest_path)

    # ------------------------------------------------------------
    # 2. PRINT INITIAL SHIP STATE
    # ------------------------------------------------------------
    print("\n=== INITIAL SHIP STATE ===")
    print(ship)

    # ------------------------------------------------------------
    # 3. TEST BASIC FUNCTIONS BEFORE A*
    # ------------------------------------------------------------
    print("\n=== BASIC CHECKS ===")
    print("Grid tuple hashable:", isinstance(ship.grid_tuple(), tuple))
    print("Initial balance difference:", ship.get_balance_difference())
    print("Heuristic value:", balance_heuristic(ship))

    moves = ship.get_valid_moves()
    print("Number of valid moves from start:", len(moves))
    if moves:
        print("Example move:", moves[0][1])

    # ------------------------------------------------------------
    # 4. RUN A* SEARCH
    # ------------------------------------------------------------
    print("\n=== RUNNING A* SEARCH ===")
    move_history, cost = a_star_search(ship, max_expansions=5000)

    if move_history is None:
        print("A* could not find a solution.")
        return

    print(f"A* found a solution with total crane cost: {cost}")
    print_moves(move_history)

    # ------------------------------------------------------------
    # 5. APPLY MOVES TO VERIFY FINAL STATE
    # ------------------------------------------------------------
    print("\n=== VERIFYING END STATE ===")
    final_ship = ship
    for move in move_history:
        final_ship = final_ship.perform_move(move.start_pos,
                                             move.end_pos,
                                             move.container_weight)

    print("\n=== FINAL SHIP STATE ===")
    print(final_ship)

    print("\nGoal reached:", final_ship.is_goal())
    print("Final balance difference:", final_ship.get_balance_difference())

if __name__ == "__main__":
    main()
