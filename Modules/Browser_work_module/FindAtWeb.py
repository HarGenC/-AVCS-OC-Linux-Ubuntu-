import webbrowser as wb
import sys

if(len(sys.argv) != 1):
    wb.open('https://www.google.com/search?q=' + sys.argv[1])