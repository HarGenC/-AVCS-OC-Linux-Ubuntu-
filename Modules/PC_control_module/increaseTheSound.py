import os
import sys

def increaseTheSound():
    if len(sys.argv) <= 2:
        os.popen("amixer -D pulse sset Master 10%+")

if __name__ == "__main__":
    increaseTheSound()