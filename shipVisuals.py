from container_ship import ContainerMove
from container_ship import ContainerShip

def format_move_log(move):
    """
    Formats a ContainerMove into a log string like: [04,01] was moved to [10,02]
    Args:
        move: A ContainerMove namedtuple or tuple of (start_pos, end_pos)
    Returns:
        String in format: [row,col] was moved to [row,col]
    """
    
    if isinstance(move, ContainerMove):
        start_pos = move.start_pos
        end_pos = move.end_pos
    elif isinstance(move, tuple) and len(move) == 2:
        start_pos, end_pos = move
    else:
        raise TypeError("move must be a ContainerMove or tuple of (start_pos, end_pos)")
    
    start_str = f"[{start_pos[0]:02d},{start_pos[1]:02d}]"
    end_str = f"[{end_pos[0]:02d},{end_pos[1]:02d}]"
    
    return f"{start_str} was moved to {end_str}"

def ship_to_visualization_grid(ship):
    """
    Converts a ContainerShip object to the grid format expected by containersVisualization.
    Returns a grid where:
    - Empty cells (0) are represented as "UNUSED"
    - Containers are represented as dicts with "weight" key
    """
    if not isinstance(ship, ContainerShip):
        raise TypeError("ship must be a ContainerShip object")
    
    shipGrid = [["NAN" for _ in range(12)] for _ in range(8)]
    
    for r in range(8):
        for c in range(12):
            weight = ship.grid[r][c]
            if weight == 0:
                shipGrid[r][c] = "UNUSED"
            else:
                shipGrid[r][c] = {"weight": weight}
    
    return shipGrid

def containersVisualization(ship_or_grid, source = None, target = None, craneParkLocation = None):   #can call in the source and the target for each turn using visualization
    """
    Visualizes a container ship. Accepts either:
    - A ContainerShip object
    - A grid (list of lists) in the visualization format
    """
    
    # Convert ContainerShip to grid format if needed
    if isinstance(ship_or_grid, ContainerShip):
        shipGrid = ship_to_visualization_grid(ship_or_grid)
    else:
        shipGrid = ship_or_grid
    
    green = "\033[92m"
    red = "\033[91m"
    original = "\033[0m"
    columnWidth = 6
    rowWidth = 6             #the size of each cell vertically and horizontally

    print("\n")
    print(" " * 9 + "XXX")   #the crane

    for row in range(8, 0, -1): #going from the top of the ship downward
        if row in (8, 1):
            rowNumber = f"{row:02d}"
        else:
            rowNumber = "  "
        
        rows = f"{rowNumber}    "

        for column in range(1, 13):
            container = shipGrid[row - 1][column - 1]

            if container == "UNUSED":    #need to show the empy space to the operator
                info = "..."
            elif container == "NAN":  
                info = "NAN"
            else:
                info = str(container["weight"])

            if source == (row, column):
                info = f"{green}{info}{original}"
            elif target == (row, column):
                info = f"{red}{info}{original}"

            rows += info.rjust(columnWidth)
        
        print(rows)
    print("\n")
    #the column headers
    columnHeader = ""
    for column in range(1, 13):
        if column in (1, 12):
            columnHeader += f"{column:02d}".rjust(columnWidth)
        else:
            columnHeader += "  ".rjust(columnWidth)
    
    print(" " * rowWidth + columnHeader)
    if craneParkLocation == "source":
        print(f"The crane starts at: {green}PARK{original}\n")
    elif craneParkLocation == "target":
        print(f"Move the crane back to: {red}PARK{original}\n")
    print("\n")

#remove everything below this line before integrating into the main codebase
def test_format_move_log():
    """Test the format_move_log function with various inputs"""
    print("=== Testing format_move_log ===\n")
    
    # Test 1: Using ContainerMove object
    move1 = ContainerMove(start_pos=(4, 1), end_pos=(10, 2), container_weight=5000, cost=15)
    result1 = format_move_log(move1)
    print(f"Test 1 (ContainerMove): {result1}")
    print(f"Expected: [04,01] was moved to [10,02]")
    
    # Test 2: Using tuple of positions
    move2 = ((1, 3), (8, 12))
    result2 = format_move_log(move2)
    print(f"Test 2 (Tuple): {result2}")
    print(f"Expected: [01,03] was moved to [08,12]")
    
    # Test 3: Single digit positions (should still zero-pad)
    move3 = ContainerMove(start_pos=(1, 1), end_pos=(2, 3), container_weight=3000, cost=10)
    result3 = format_move_log(move3)
    print(f"Test 3 (Single digits): {result3}")
    print(f"Expected: [01,01] was moved to [02,03]")
    # Test 4: Your example from the log
    move4 = ContainerMove(start_pos=(1, 4), end_pos=(3, 3), container_weight=4000, cost=12)
    result4 = format_move_log(move4)
    print(f"Test 4 (Your example): {result4}")
    print(f"Expected: [01,04] was moved to [03,03]")
    
    print("=== All tests complete ===")

def main():
    from container_ship import ContainerShip
    
    # Test format_move_log
    test_format_move_log()
    
    # Original visualization test
    print("\n=== Ship Visualization ===")
    ship = ContainerShip("manifests/testManifest.txt")
    containersVisualization(ship)

if __name__ == "__main__":
    main()