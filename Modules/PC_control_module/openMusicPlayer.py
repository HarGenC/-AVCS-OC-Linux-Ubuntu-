import subprocess
import sys

def openMusicPlayer():
    if len(sys.argv) <= 2:
        musicPlayer = "rhythmbox"
        subprocess.call([musicPlayer])

if __name__ == "__main__":
    openMusicPlayer()