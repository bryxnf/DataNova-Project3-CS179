import os
import time

class Logger:

    # Create Logs folder in SAME directory as main.py
    def __init__(self):
        self.lines = []

        baseDir = os.path.dirname(os.path.abspath(__file__))
        self.logsDir = os.path.join(baseDir, "logs")
        os.makedirs(self.logsDir, exist_ok=True)

    def timestamp(self) -> str:
        return time.strftime("%m %d %Y: %H:%M")
    
    # Logs with the timestamp
    def log(self, message: str) -> None:
        line = f"{self.timestamp()} {message}"
        self.lines.append(line)
        print(line)

    # Logs without timestamp
    def logRaw(self, message: str) -> None:
        self.lines.append(message)
        print(message)

    # Filename example: KeoghsPort10_18_2023_0204.txt
    def writeToFile(self) -> str:
        filename = f"KeoghsPort{time.strftime('%m_%d_%Y_%H%M')}.txt"
        full_path = os.path.join(self.logsDir, filename)

        with open(full_path, "w", encoding="utf-8") as f:
            for line in self.lines:
                f.write(line + "\n")

        return full_path
    
    def progShutDown(self) -> None:
        # Basically we will remove the redudency of calling end
        # function multiple places and instead call this when we get the error
        return None
