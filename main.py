import os
import sys
from manifestParser import ManifestParser
from container_ship import ContainerShip
from astar import a_star_search
from shipVisuals import loadManifest, containersVisualization
from manifestExporter import save_manifest_to_desktop
from log import Logger


def format_entry(entry):
    (row, col), weight, desc = entry
    return f"[{row:02d},{col:02d}], {{{weight:05d}}}, {desc}"

def main():

    firstIteration = True
    endTheEntireProg = ""

    while(endTheEntireProg == ""):
        logger = Logger()
        if firstIteration:
            logger.log("Program was started.")
            firstIteration = False

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

        if moveHistory is None:
            logger.log(f"Balance solution was not found for {os.path.basename(filePath)}")
            logger.log("A* search stopped: search space grew too large or the manifest data may contain an error.")
            return
        parkToFirstCost = 0
        lastToParkCost = 0
        if moveHistory:
            # Cost to move from PARK to the first container position
            parkToFirstCost = ship.calculate_park_to_position_cost(moveHistory[0].start_pos)
            # Cost to move from the last container position back to PARK
            lastToParkCost = ship.calculate_position_to_park_cost(moveHistory[-1].end_pos)
        totBalMin += parkToFirstCost + lastToParkCost

        logger.log(f"Balance solution found, it will require {totalBalMove} moves/{totBalMin} minutes.")
        

        resp = input("Press Enter to begin the move sequence, or type anything to cancel: ").strip()

        # If user pressed anything but enter then we end the program
        if resp != "":
            print("Move sequence cancelled.")
            return 

        visualGrid = loadManifest(filePath)
        currShip = ship

        moveIndex = 0

        for i in range(1, totalBalMove + 1):
            startPos, endPos, containerWeight, costToMoveCurrBox = (
                moveHistory[moveIndex].start_pos,
                moveHistory[moveIndex].end_pos,
                moveHistory[moveIndex].container_weight,
                moveHistory[moveIndex].cost
            )

            startFmt = f"[{startPos[0]:02d}, {startPos[1]:02d}]"
            endFmt = f"[{endPos[0]:02d}, {endPos[1]:02d}]"
            
            if i == 1:
                containersVisualization(visualGrid, target=startPos, craneParkLocation="source")
                logger.log(f"{i} of {totalBalMove}: Move from PARK to {startFmt}, {parkToFirstCost} minutes")
            elif i == totalBalMove:
                containersVisualization(visualGrid, source=endPos, target=None, craneParkLocation="target")
                logger.log(f"{i} of {totalBalMove}: Move from {endFmt} to PARK, {lastToParkCost} minutes")    
            else:
                containersVisualization(visualGrid, source=startPos, target=endPos, craneParkLocation=None)
                logger.log(f"{i} of {totalBalMove}: {startFmt} was moved to {endFmt}, {costToMoveCurrBox} minutes")

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
                
                if moveIndex < len(moveHistory) - 1:
                    moveIndex += 1


            print("If you want to record a note about this move, type it now. Otherwise, press \"Enter\" to continue:")
            description = input().strip()
            if description:
                logger.log(description)
        
        try:
            outputPath = save_manifest_to_desktop(currShip, visualGrid, shipName)
            logger.log(f"Finished a Cycle. Manifest {os.path.basename(outputPath)} was written to desktop, and a reminder pop-up to operator to send file was displayed.")
        except Exception as e:
            logger.log(f"ERROR: Failed to save manifest to desktop: {e}")
            logger.logRaw(f"Error details: {str(e)}")
            logger.progShutDown(shipName)

        logger.progShutDown(shipName)
        
        endTheEntireProg = input("Press \"Enter\" to continue the program, or type any key to quit: ").strip()

if __name__ == "__main__":
    main()
