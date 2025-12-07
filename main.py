import os
import sys
from manifestParser import ManifestParser
from container_ship import ContainerShip
from astar import a_star_search
from shipVisuals import format_move_log, containersVisualization
from log import Logger
import time


def format_entry(entry):
    (row, col), weight, desc = entry
    return f"[{row:02d},{col:02d}], {{{weight:05d}}}, {desc}"

def main():
    logger = Logger()

    logger.log("Program was started.")

    filename = input("Enter the path of the Ship file: ").strip()
    logger.log(f"User entered path: {filename}")
    
    if not filename:
        logger.log("Path provided was not found.")
        logger.progShutDown()
        sys.exit(1)
    
    if os.path.isabs(filename):
        filePath = filename
    else:
        baseDir = os.path.dirname(os.path.abspath(__file__))
        filePath = os.path.join(baseDir, filename)

    if not os.path.exists(filePath):
        logger.log(f"ERROR: File does not exist: {filePath}")
        logger.progShutDown()
        sys.exit(1)

    parser = ManifestParser()
    parserFile = parser.parse_manifest(filePath)

    totalContainers = len(parserFile)
    logger.log(f"Manifest {os.path.basename(filePath)} is opened, there are {totalContainers} containers on the ship.")

    ship = ContainerShip(filePath)
    moveHistory, totBalMin, totalBalMove = a_star_search(ship, max_expansions=50000)

    if moveHistory is None: # THINK ABOUT THIS LATER
        logger.log("A* could not find a solution.")
        return

    # If the ship balance was not found
    logger.log(f"Balance solution was not found for {os.path.basename(filePath)}")
    # else we do this
    logger.log(f"Balance solution found, it will require {totalBalMove + 2} moves/{totBalMin} minutes.")

    print(moveHistory)

    # for i, move in enumerate(moveHistory, 1):   
    #     print(f"Current move: {move}")

    logger.progShutDown()


if __name__ == "__main__":
    main()