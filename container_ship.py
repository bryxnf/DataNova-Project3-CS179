from collections import namedtuple
from typing import List, Tuple, Optional
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

        #converts data to (row,col,weight) tuples
        manifest_data = [(pos[0],pos[1],weight) for pos, weight, desc in manifest_entries]


        #initialize grid/weights
        self.grid = [[0 for _ in range(MAX_COLS)] for _ in range(MAX_ROWS)]
        self.total_weight = 0
        self.port_weight = 0
        self.max_row = MAX_ROWS
        self.max_col = MAX_COLS

        #to produce the grid
        self.parse_manifest(manifest_data)

    #created this function to make the tuple of tuples unchangleable(so i can compare the ship for search algorithms)
    def grid_tuple(self):
        return tuple(tuple(row) for row in self.grid())
    
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
    def parse_manifest(self, manifest_data: List[Tuple[int, int, int]]):
        for r, c, w in manifest_data:
            r0 = r -1
            c0 = c -1
            if 0 <= r0 < MAX_ROWS and 0 <= c0 < MAX_COLS:
                if self.grid[r0][c0] != 0:
                    print(f"Warning: overriding container at ({r}, {c})")
                self.grid[r0][c0] = w
                self.total_weight += w
                if c0 < (MAX_COLS // 2):
                    self.port_weight +=w
                else:
                    self.starboard_weight += w
            else: 
                print(f"Warning: invalid position ({r},{c}) ignored.")

    #to check if there is nothing above the cur container(will be used for horizontal sliding)
    def if_exposed(self,row_idx: int, col_idx: int)-> bool:
        if self.grid[row_idx][col_idx]:
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
    
    
    
        
