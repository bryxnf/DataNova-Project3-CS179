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

    def grid_tuple(self):
        return tuple(tuple(row) for row in self.grid())
    
    def get_top_container(self,col: int)-> Tuple[Optional[Tuple[int, int]], int]:
        for r in range(MAX_ROWS - 1, -1, -1):
            if self.grid[r][col] != 0:
                return (r+1, col + 1), self.grid[r][col]
        return None, 0
        
    def get_next_empty(self,col: int)-> Optional[Tuple[int, int]]:
        for r in range(MAX_ROWS):
            if self.grid[r][col] == 0:
                return (r+1, col + 1)
        return None
