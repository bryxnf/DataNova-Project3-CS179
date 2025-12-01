def loadManifest(shipCase):    
    shipGrid = [["NAN" for _ in range(12)] for _ in range(8)]

    with open(shipCase, "r") as manifest:
        for containerInfo in manifest:            
            #need to separate the parts because each line has [01,01], {00000}, NAN structure
            information = containerInfo.strip().split(',')
            rowInfo = information[0][1:3]
            columnInfo = information[1][0:2]
            tareInfo = int(information[2].strip("{} "))
            itemInfo = information[3].strip()

            rows = int(rowInfo)
            columns = int(columnInfo)

            if itemInfo in ["NAN", "UNUSED"]:
                shipGrid[rows - 1][columns - 1] = itemInfo
            else:
                shipGrid[rows - 1][columns - 1] = {
                    "weight": tareInfo,
                    "info": itemInfo}
                
    return shipGrid

def containersVisualization(shipGrid, source = None, target = None, craneParkLocation = None):   #can call in the source and the target for each turn using visualization
    green = "\033[92m"
    red = "\033[91m"
    original = "\033[0m"
    columnWidth = 6
    rowWidth = 6             #the size of each cell vertically and horizontally

    print("\n")
    print(" " * 9 + "XXX")   #the crane

    for row in range(8, 0, -1): #going from the top of the ship downward
        if row in (8, 1):
            rowNumber = f"{row:02d}"
        else:
            rowNumber = "  "
        
        rows = f"{rowNumber}    "

        for column in range(1, 13):
            container = shipGrid[row - 1][column - 1]

            if container == "UNUSED":    #need to show the empy space to the operator
                info = "..."
            elif container == "NAN":  
                info = "NAN"
            else:
                info = str(container["weight"])

            if source == (row, column):
                info = f"{green}{info}{original}"
            elif target == (row, column):
                info = f"{red}{info}{original}"

            rows += info.rjust(columnWidth)
        
        print(rows)
    print("\n")
    #the column headers
    columnHeader = ""
    for column in range(1, 13):
        if column in (1, 12):
            columnHeader += f"{column:02d}".rjust(columnWidth)
        else:
            columnHeader += "  ".rjust(columnWidth)
    
    print(" " * rowWidth + columnHeader)
    if craneParkLocation == "source":
        print(f"The crane starts at: {green}PARK{original}\n")
    elif craneParkLocation == "target":
        print(f"Move the crane back to: {red}PARK{original}\n")
    print("\n")

def main():
    grid = loadManifest("testFiles/ShipCase5.txt")
    containersVisualization(grid)

if __name__ == "__main__":
    main()