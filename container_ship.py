from collections import namedtuple, deque
from typing import List, Tuple, Optional, Dict, Set
from manifestParser import ManifestParser

MAX_ROWS = 8
MAX_COLS = 12

#this will be use to make stores and print easily
ContainerMove = namedtuple('ContainerMove',['start_pos','end_pos','container_weight','cost'])

class ContainerShip:
    def __init__(self, manifest_file: str): 
        #initialize the ship with the manifest file
        parser = ManifestParser()
        manifest_entries = parser.parse_manifest(manifest_file)

        # keep (row, col, weight, description) tuples
        manifest_data = [(pos[0], pos[1], weight, desc) for pos, weight, desc in manifest_entries]


        #initialize grid/weights
        self.grid = [[0 for _ in range(MAX_COLS)] for _ in range(MAX_ROWS)]
        self.total_weight = 0 #curr total weight
        self.port_weight = 0 #left hand side
        self.starboard_weight = 0 #right hand side
        self.max_row = MAX_ROWS
        self.max_col = MAX_COLS

        #saves original total weight (Po + So) for legal threshold
        self.original_total_weight: int = 0

        #cache for minial possible imbalance (computed on demand)
        self.min_possible_imbalance: Optional[int] = None

        #metadata grid stores description/labels (e.g., UNUSED, NAN, cargo description)
        self.metadata = [["UNUSED" for _ in range(MAX_COLS)] for _ in range(MAX_ROWS)]

        #to produce the grid
        self.parse_manifest(manifest_data)

        #store original total after initial parse
        self.original_total_weight = self.total_weight

    #created this function to make the tuple of tuples unchangleable(so i can compare the ship for search algorithms)
    def grid_tuple(self):
        return tuple(tuple(row) for row in self.grid)
    
    #finds the top container within the column
    def get_top_container(self,col: int)-> Tuple[Optional[Tuple[int, int]], int]:
        for r in range(MAX_ROWS - 1, -1, -1):
            if self.grid[r][col] != 0:
                return (r+1, col + 1), self.grid[r][col]
        return None, 0

    #finds the first empty slot from the bottom up in a column  
    def get_next_empty(self,col: int)-> Optional[Tuple[int, int]]:
        for r in range(MAX_ROWS):
            if self.grid[r][col] == 0:
                return (r+1, col + 1)
        return None
    
    #places the data into each grid within the ship
    def parse_manifest(self, manifest_data: List[Tuple[int, int, int, str]]):
        for r, c, w, desc in manifest_data:
            r0 = r -1
            c0 = c -1
            if 0 <= r0 < MAX_ROWS and 0 <= c0 < MAX_COLS:
                if self.grid[r0][c0] != 0:
                    # silently override if container already exists
                    pass
                self.grid[r0][c0] = w
                self.metadata[r0][c0] = desc if desc else ("UNUSED" if w == 0 else "")
                self.total_weight += w
                if c0 < (MAX_COLS // 2):
                    self.port_weight +=w
                else:
                    self.starboard_weight += w
            #ignore invalid positions

    #to check if there is nothing above the cur container(will be used for horizontal sliding)
    def is_exposed(self,row_idx: int, col_idx: int)-> bool:
        if self.grid[row_idx][col_idx] == 0:
            return False
        for rr in range(row_idx + 1, MAX_ROWS):
            if self.grid[rr][col_idx] != 0:
                return False
        return True
    
    #to check whether its the first container or has a container below it
    def is_supported(self,row_idx: int, col_idx: int) -> bool:
        if row_idx == 0:
            return True
        return self.grid[row_idx - 1][col_idx] != 0 
    
    #returns the |Pr-Sr|
    def get_balance_difference(self)-> int:
        return abs(self.port_weight - self.starboard_weight)

    #function to get the cost of the move
    def calculate_move_cost(self, start_pos: Tuple[int, int], end_pos: Tuple[int,int], slide:bool = False)-> int:
        if slide:
            return 0
        r1, c1 = start_pos
        r2, c2 = end_pos

        # Cost is Manhattan distance: horizontal + vertical change
        horizontal = abs(c1 - c2)
        vertical = abs(r1 - r2)
        return horizontal + vertical
    
    #PARK position is at row 9, column 1
    #Cost to move from PARK to a position: move horizontally to column, then down to row
    #Note: Subtract 1 because we don't count the PARK row itself in the distance
    def calculate_park_to_position_cost(self, position: Tuple[int, int]) -> int:
        """Calculate cost to move crane from PARK to a position"""
        r, c = position
        park_col = 1
        # Move horizontally from PARK column to target column
        horizontal = abs(c - park_col)
        # Move down from PARK (row 9) to target row
        # Distance is (MAX_ROWS + 1) - r - 1 because we don't count PARK row itself
        down_to_position = (MAX_ROWS + 1) - r - 1
        return horizontal + down_to_position
    
    #Cost to move from a position back to PARK: move up to row 9, then horizontally to column 1
    #Note: Subtract 1 because we don't count the PARK row itself in the distance
    def calculate_position_to_park_cost(self, position: Tuple[int, int]) -> int:
        """Calculate cost to move crane from a position back to PARK (row 9, col 1)"""
        r, c = position
        park_col = 1
        # Move up from position row to PARK (row 9)
        # Distance is (MAX_ROWS + 1) - r - 1 because we don't count PARK row itself
        up_to_park = (MAX_ROWS + 1) - r - 1
        # Move horizontally to PARK column (1)
        horizontal = abs(c - park_col)
        return up_to_park + horizontal
    
    #this will return a new ContainerShip state after moving the container at start_pos to end_pos

    def perform_move(self,start_pos: Tuple[int, int], end_pos: Tuple[int,int], weight: int)-> 'ContainerShip':
        #we create a copy so that the new move does not modify the orginial ship aka self.grid
        new_ship = ContainerShip.__new__(ContainerShip)
        new_ship.grid = [row[:] for row in self.grid]
        new_ship.total_weight = self.total_weight
        new_ship.port_weight = self.port_weight
        new_ship.starboard_weight = self.starboard_weight
        new_ship.max_row = self.max_row
        new_ship.max_col = self.max_col
        new_ship.original_total_weight = self.original_total_weight
        new_ship.min_possible_imbalance = None  # computed on demand
        new_ship.metadata = [row[:] for row in self.metadata]

        r1,c1 = start_pos[0] - 1, start_pos[1] -1
        r2,c2 = end_pos[0] - 1, end_pos[1] -1

        #test cases
        if new_ship.grid[r1][c1] != weight:
            raise ValueError(f"Attempted to move but start cell ({start_pos}) doesnt contain the given weight")
        if new_ship.grid[r2][c2] != 0:
            raise ValueError("Attempted to move into a non-empty slot")
        
        #excecutes the move
        new_ship.grid[r1][c1] = 0
        new_ship.grid[r2][c2] = weight

        # Move metadata (container description or NAN marker) along with the container
        start_meta = new_ship.metadata[r1][c1]
        new_ship.metadata[r1][c1] = "UNUSED"  # Source becomes empty
        # Copy metadata (including NAN markers) to destination, default to UNUSED if None
        if start_meta is not None:
            new_ship.metadata[r2][c2] = start_meta
        else:
            new_ship.metadata[r2][c2] = "UNUSED"

        left_half = (MAX_COLS // 2)  # columns 0..left_half-1 are port
        start_is_port = (c1 < left_half)
        end_is_port = (c2 < left_half)
        if start_is_port and not end_is_port:
            new_ship.port_weight -= weight
            new_ship.starboard_weight += weight
        elif not start_is_port and end_is_port:
            new_ship.starboard_weight -= weight
            new_ship.port_weight += weight

        #returns newship
        new_ship.total_weight = new_ship.port_weight + new_ship.starboard_weight
        return new_ship
    
    #This gives us the sliding feature
    """
    For a given cell (0-indexed) that contains an exposed container, return a list of possible slide moves.
    Each entry is (start_pos_1indexed, end_pos_1indexed, weight).
    Slide targets are any column on the same row such that:
        - all cells between start and target (exclusive) on that row are empty
        - target cell is empty
        - target cell would be supported (bottom row or cell below non-empty)
    """
    def get_horizontal_slides_from_cell(self, row_idx: int, col_idx: int) -> List[Tuple[Tuple[int, int], Tuple[int, int], int]]:
        results = []
        weight = self.grid[row_idx][col_idx]
        if weight == 0:
            return results
        if not self.is_exposed(row_idx, col_idx):
            return results

        start_pos = (row_idx + 1, col_idx + 1)

        #scan LEFT until blocked - add ALL valid positions, not just the furthest
        c = col_idx - 1
        while c >= 0:
            if self.grid[row_idx][c] != 0:
                break  # blocked
            if self.is_supported(row_idx, c):
                results.append((start_pos, (row_idx + 1, c + 1), weight))
            c -= 1

        #scan RIGHT until blocked - add ALL valid positions, not just the furthest
        c = col_idx + 1
        while c < self.max_col:
            if self.grid[row_idx][c] != 0:
                break
            if self.is_supported(row_idx, c):
                results.append((start_pos, (row_idx + 1, c + 1), weight))
            c += 1

        return results
    
    #this will get the valid moves 
    """
    Generate all legal single-container moves from current state:
        - Crane pick-and-place moves (only top container of a column -> top empty slot of another column)
        - Horizontal sliding moves (as per get_horizontal_slides_from_cell) with cost=0
    Returns list of tuples: (new_ship, ContainerMove)
    """
    def get_valid_moves(self):
        moves = []

        # 1)This gives us the valid crane moves (aka only top containers)
        for start_col in range(self.max_col):
            start_pos, weight = self.get_top_container(start_col)
            if not start_pos:
                continue
            for end_col in range(self.max_col):
                if end_col == start_col:
                    continue
                end_pos = self.get_next_empty(end_col)
                if not end_pos:
                    continue
                cost = self.calculate_move_cost(start_pos, end_pos, slide=False)
                new_ship = self.perform_move(start_pos, end_pos, weight)
                move_obj = ContainerMove(start_pos, end_pos, weight, cost)
                moves.append((new_ship, move_obj))

        # 2)This gives us the Horizontal sliding moves (scans every cell)
        for r in range(self.max_row):
            for c in range(self.max_col):
                if self.grid[r][c] == 0:
                    continue
                # get potential slides from this exposed cell
                slides = self.get_horizontal_slides_from_cell(r, c)
                for start_pos, end_pos, weight in slides:
                    # double-check end_pos emptiness & support
                    er, ec = end_pos
                    er_idx, ec_idx = er - 1, ec - 1
                    if self.grid[er_idx][ec_idx] != 0:
                        continue
                    new_ship = self.perform_move(start_pos, end_pos, weight)
                    # Horizontal slides cost the horizontal distance (1 minute per column)
                    slide_cost = abs(start_pos[1] - end_pos[1])
                    move_obj = ContainerMove(start_pos, end_pos, weight, slide_cost)
                    moves.append((new_ship, move_obj))

        return moves
    
    #this uses breadth first search exploration of reachable states (unweighted) to find the minimal |Pr-Sr|
    #its also bounded meaning if it reaches a boundary it just returns the best so far.
    def compute_min_possible_imbalance(self, max_expansions: int = 200000, threshold: Optional[float] = None) -> int:
        if self.min_possible_imbalance is not None:
            return self.min_possible_imbalance

        start_grid = self.grid_tuple()
        start_diff = abs(self.port_weight - self.starboard_weight)
        best_diff = start_diff

        visited: Set[Tuple[Tuple[int, ...], ...]] = {start_grid}
        queue = deque()
        queue.append(self)

        expansions = 0
        #BFS loop, keeps exploring while theres still states to explore
        while queue and expansions < max_expansions:
            ship = queue.popleft()
            expansions += 1

            # update best diff
            diff = abs(ship.port_weight - ship.starboard_weight)
            if diff < best_diff:
                best_diff = diff
                if best_diff == 0:
                    break
                # Early exit if we found a state that meets the threshold
                if threshold is not None and best_diff < threshold:
                    break

            # expand neighbors (unweighted BFS)
            for new_ship, _move in ship.get_valid_moves():
                g = new_ship.grid_tuple()
                if g in visited:
                    continue
                visited.add(g)
                queue.append(new_ship)

        # cache and return
        self.min_possible_imbalance = best_diff
        return best_diff
    
    """
    Legal goal:
        - If |Pr - Sr| < 0.10 * (Po + So) -> goal (legal threshold using original totals)
        - OR if |Pr - Sr| == minimal possible imbalance among reachable states -> goal
    This function computes the minimal possible imbalance lazily using compute_min_possible_imbalance().
    """
    def is_goal(self) -> bool:
        # quick accept if empty ship
        if self.original_total_weight == 0:
            return True

        diff = abs(self.port_weight - self.starboard_weight)
        threshold = 0.10 * self.original_total_weight
        if diff < threshold:
            return True

        # compute minimal possible imbalance with a smaller expansion limit to avoid hanging
        # Use a much smaller limit when called from is_goal() to keep it fast
        # Also pass the threshold so BFS can exit early if it finds a state that meets it
        min_diff = self.compute_min_possible_imbalance(max_expansions=5000, threshold=threshold)
        return diff == min_diff
    
    #basic string representation without visual formatting
    def __repr__(self):
        return f"ContainerShip(Port:{self.port_weight}, Starboard:{self.starboard_weight}, Total:{self.total_weight}, Diff:{self.get_balance_difference()})"
