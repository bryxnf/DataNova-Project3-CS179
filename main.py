import os
import sys
from manifestParser import ManifestParser
from container_ship import ContainerShip
from astar import a_star_search
from shipVisuals import loadManifest, containersVisualization
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
        logger.progShutDown("UNKNOWN_SHIP")
        sys.exit(1)
    
    if os.path.isabs(filename):
        filePath = filename
    else:
        baseDir = os.path.dirname(os.path.abspath(__file__))
        filePath = os.path.join(baseDir, filename)

    if not os.path.exists(filePath):
        logger.log(f"ERROR: File does not exist: {filePath}")
        logger.progShutDown("UNKNOWN_SHIP")
        sys.exit(1)

    shipName = os.path.basename(filePath).replace(".txt", "")

    parser = ManifestParser()
    parserFile = parser.parse_manifest(filePath)

    totalContainers = len(parserFile)
    logger.log(f"Manifest {os.path.basename(filePath)} is opened, there are {totalContainers} containers on the ship.")

    ship = ContainerShip(filePath)
    moveHistory, totBalMin, totalBalMove = a_star_search(ship, max_expansions=50000)

    if moveHistory is None: # THINK ABOUT THIS LATER
        logger.log("A* could not find a solution because node expansion was too long or there was an error in the manifest file")
        return

    # If the ship balance was not found
    # logger.log(f"Balance solution was not found for {os.path.basename(filePath)}")
    # else we do this
    logger.log(f"Balance solution found, it will require {totalBalMove} moves/{totBalMin} minutes.")

    visualGrid = loadManifest(filePath)
    containersVisualization(visualGrid, craneParkLocation="source")

    resp = input("Press Enter to begin the move sequence, or type anything to cancel: ").strip()

    # If user pressed anything but enter then we end the program
    if resp != "":
        print("Move sequence cancelled.")
        return 

    totalMoves = len(moveHistory)
    currShip = ship

    for i, move in enumerate(moveHistory, 1):
        startPos, endPos, containerWeight, _ = move
        currShip = currShip.perform_move(startPos, endPos, containerWeight)

        sr, sc = startPos
        tr, tc = endPos

        cell = visualGrid[sr - 1][sc - 1]

        if isinstance(cell, dict):
            container_dict = cell
        else:
            container_dict = {"weight": containerWeight, "info": ""}

        visualGrid[sr - 1][sc - 1] = "UNUSED"
        visualGrid[tr - 1][tc - 1] = container_dict
        containersVisualization(visualGrid, source=startPos, target=endPos, craneParkLocation="target" if i == totalMoves else None)


        # Fix this visualization part        
        # currShip = currShip.perform_move(startPos,endPos, containerWeight)
        # containersVisualization(currShip, source=startPos, target=endPos, craneParkLocation="target" if i == totalMoves else None)
        startFmt = f"[{startPos[0]:02d}, {startPos[1]:02d}]"
        endFmt = f"[{endPos[0]:02d}, {endPos[1]:02d}]"

        logger.log(f"{startFmt} was moved to {endFmt}")
        print("If you want to record a note about this move, type it now. Otherwise, press \"Enter\" to continue:")
        description = input().strip()
        if description:
            logger.log(description)
    
    logger.log(f"Finished a Cycle. Manifest HMMAlgecirasOUTBOUND.txt was written to desktop, and a reminder pop-up to operator to send file was displayed.")

    logger.progShutDown(shipName)


if __name__ == "__main__":
    main()
