import os
from container_ship import ContainerShip
from astar import a_star_search
from shipVisuals import format_move_log, containersVisualization

def main():
    # ------------------------------------------------------------
    # 1. LOAD MANIFEST
    # ------------------------------------------------------------
    manifest_path = "manifests/ShipCase4.txt"  # Change this to your manifest file
    if not os.path.exists(manifest_path):
        print(f"ERROR: Manifest file not found: {manifest_path}")
        return
    
    print("Loading ship from manifest...")
    ship = ContainerShip(manifest_path)
    
    # ------------------------------------------------------------
    # 2. DISPLAY INITIAL SHIP STATE
    # ------------------------------------------------------------
    print("\n=== INITIAL SHIP STATE ===")
    containersVisualization(ship)
    print(f"Initial balance difference: {ship.get_balance_difference()}")
    print(f"Port weight: {ship.port_weight}, Starboard weight: {ship.starboard_weight}")
    
    # ------------------------------------------------------------
    # 3. RUN A* SEARCH
    # ------------------------------------------------------------
    print("\n=== RUNNING A* SEARCH ===")
    move_history, cost, num_moves = a_star_search(ship, max_expansions=5000)
    
    if move_history is None:
        print("A* could not find a solution.")
        return
    
    print(f"A* found a solution with {num_moves} moves and total crane cost: {cost} minutes")
    
    # ------------------------------------------------------------
    # 4. EXECUTE MOVES STEP-BY-STEP
    # ------------------------------------------------------------
    current_ship = ship
    total_moves = len(move_history)
    
    print(f"\n=== Executing {total_moves} moves ===")
    print("Press Enter to execute each move. Press Ctrl+C to exit.\n")
    
    for i, move in enumerate(move_history, 1):
        input(f"Press Enter to execute move {i} of {total_moves}...")
        
        # Display the move in log format
        move_log = format_move_log(move)
        print(f"\nMove {i}: {move_log}")
        print(f"  Container weight: {move.container_weight} lbs")
        print(f"  Move cost: {move.cost} minutes")
        
        # Execute the move
        current_ship = current_ship.perform_move(
            move.start_pos,
            move.end_pos,
            move.container_weight
        )
        
        # Show visualization with source and target highlighted
        containersVisualization(
            current_ship, 
            source=move.start_pos, 
            target=move.end_pos,
            craneParkLocation="target" if i == total_moves else None
        )
        
        # Show current ship state
        print(f"Balance difference: {current_ship.get_balance_difference()}")
        print(f"Port weight: {current_ship.port_weight}, Starboard weight: {current_ship.starboard_weight}\n")
    
    # ------------------------------------------------------------
    # 5. FINAL STATE
    # ------------------------------------------------------------
    print("=== ALL MOVES COMPLETED ===")
    print(f"Final balance difference: {current_ship.get_balance_difference()}")
    print(f"Goal reached: {current_ship.is_goal()}")
    print(f"Total moves: {num_moves}")
    print(f"Total cost: {cost} minutes")

if __name__ == "__main__":
    main()

