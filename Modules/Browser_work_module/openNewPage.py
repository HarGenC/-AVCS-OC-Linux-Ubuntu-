import os

def openNewPage():
    os.popen('firefox --new-tab --url about:newtab')

if __name__ == '__main__':
    openNewPage()