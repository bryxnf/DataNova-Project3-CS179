import os
from container_ship import ContainerShip, MAX_ROWS, MAX_COLS

#returns full path to the saved manifest file
def save_manifest_to_desktop(ship: ContainerShip, visual_grid, ship_name: str) -> str:
    # Get desktop path and create filename with OUTBOUND in all caps
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    output_path = os.path.join(desktop_path, f"{ship_name}_OUTBOUND.txt")
    
    # Generate manifest lines with updated positions
    manifest_lines = []
    for row in range(1, MAX_ROWS + 1):
        for col in range(1, MAX_COLS + 1):
            r, c = row - 1, col - 1
            weight = ship.grid[r][c]
            
            # Get description from visual grid
            cell = visual_grid[r][c]
            if weight == 0:
                desc = cell if isinstance(cell, str) else "UNUSED"
            else:
                desc = cell.get("info", "") if isinstance(cell, dict) else ""
            
            manifest_lines.append(f"[{row:02d},{col:02d}], {{{weight:05d}}}, {desc}")
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(manifest_lines))
    
    
    return output_path

