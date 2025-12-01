def ship_to_visualization_grid(ship):
    """
    Converts a ContainerShip object to the grid format expected by containersVisualization.
    Returns a grid where:
    - Empty cells (0) are represented as "UNUSED"
    - Containers are represented as dicts with "weight" key
    """
    from container_ship import ContainerShip
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
    from container_ship import ContainerShip
    
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

def main():
    from container_ship import ContainerShip
    ship = ContainerShip("manifests/testManifest.txt")
    containersVisualization(ship)

if __name__ == "__main__":
    main()