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