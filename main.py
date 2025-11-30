import os
import sys
from manifestParser import ManifestParser


# def Menu():
#     print("Please choose the language you want to see: ")
#     userInp = input()
#     return None

def format_entry(entry):
    (row, col), weight, desc = entry
    return f"[{row:02d},{col:02d}], {{{weight:05d}}}, {desc}"

def main():
    print("===Welcome to DataNova Ship Balancer===")
    filename = input("Enter the path of the Ship file: ").strip()

    if not filename:
        print("No path provided, exiting.")
        sys.exit(1)
    
    if os.path.isabs(filename):
        filePath = filename
    else:
        baseDir = os.path.dirname(os.path.abspath(__file__))
        filePath = os.path.join(baseDir, filename)

    if not os.path.exists(filePath):
        print(f"ERROR: File does not exist:\n  {filePath}")
        sys.exit(1)
    
    parser = ManifestParser()
    parserFile = parser.parse_manifest(filePath)

    print(f"\nParsed entries from: {filePath}\n")
    for entry in parserFile:
        print(format_entry(entry))

if __name__ == "__main__":
    main()