import os
import sys
from manifestParser import ManifestParser
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
        logger.log("Program was shut down.")
        logPath = logger.writeToFile()

        logger.logRaw(f"\nSession log written to: {logPath}")
        sys.exit(1)
    
    if os.path.isabs(filename):
        filePath = filename
    else:
        baseDir = os.path.dirname(os.path.abspath(__file__))
        filePath = os.path.join(baseDir, filename)

    if not os.path.exists(filePath):
        logger.log(f"ERROR: File does not exist: {filePath}")
        logger.log("Program was shut down.")
        logPath = logger.writeToFile()

        logger.logRaw(f"\nSession log written to: {logPath}")
        sys.exit(1)

    parser = ManifestParser()
    parserFile = parser.parse_manifest(filePath)

    totalContainers = len(parserFile)
    logger.log(f"Manifest {os.path.basename(filePath)} is opened, there are {totalContainers} containers on the ship.")

    for entry in parserFile:
        print(format_entry(entry))

    logger.log("Program was shut down.")
    logPath = logger.writeToFile()

    logger.logRaw(f"\nSession log written to: {logPath}")


if __name__ == "__main__":
    main()