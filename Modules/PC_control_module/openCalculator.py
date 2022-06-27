import subprocess
import sys

def openCalculator():
    if len(sys.argv) <= 2:
        calculator = "gnome-calculator"
        subprocess.call([calculator])

if __name__ == "__main__":
    openCalculator()