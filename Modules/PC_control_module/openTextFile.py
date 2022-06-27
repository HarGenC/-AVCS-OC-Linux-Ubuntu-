import subprocess
import sys

def openTextFile():
    if len(sys.argv) <= 2:
        createTextFile = "gedit"
        subprocess.call([createTextFile])

if __name__ == "__main__":
    openTextFile()