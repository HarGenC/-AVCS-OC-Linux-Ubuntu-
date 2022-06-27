import subprocess
from ConnectingModule import *
from ResultOutput import *
from CommandSearch import *
from ParameterSeparation import *
from HistoryDisplay import *

def CommandExecution(text, pythonBin, path, resultOutput, args=None):
    try:
        if(args!=None):
            result = subprocess.run([pythonBin, path, args])
        else:
            result = subprocess.run([pythonBin, path])
        if result.returncode == 0:
            resultOutput.showAcceptMsg("Команда выполнена успешно!")
            recordHistory("history.json", text)
        else:
            resultOutput.showErrorMsg("Error: ошибка в выполнении команды!")
            recordHistory("unrecognizedСommands.json", text)
    except :
        recordHistory("unrecognizedСommands.json", text)

def runCommand(text: str, itm, resultOutput, mainWindow):
    command = commandSearch(text, ModuleList())
    if command != None:
        parameter = parameterSeparation(text, command)
        th = Thread(target = CommandExecution, args=(text, "/usr/bin/python3", command.path, resultOutput, parameter))
        th.start()
        
    else:
        command = internalCommandSearch(text, itm)
        if command != None:
            command.func()
            recordHistory("history.json", text)
        else: 
            resultOutput.showErrorMsg("Команда не найдена")
            resultOutput.changeIconToRed()
            recordHistory("unrecognizedСommands.json", text)
    updateHistory(mainWindow)
