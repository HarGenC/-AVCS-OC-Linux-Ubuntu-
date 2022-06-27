import json
from CommandSearch import *
from ModulesAndCommandsEditor import *

def LoadFile(file):
    data = ""
    with open(file, "r",  encoding='utf-8') as file:
                data = json.load(file)
    return data

def OverwriteFile(file, data):
    with open(file, "w",  encoding='utf-8') as writeFile:
                json.dump(data, writeFile, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))

def ExistNameCommandAtModule(i, data, nameCommand):
    countCommands = len(data["Modules"][i])
    for j in range(1, countCommands):
        if (data["Modules"][i][j]["name"] == nameCommand):
                return True
    return False

def ExistVoiceResponseAtModule(voiceResponseIterator, module, voiceResponse):
    countCommands = len(module)
    for j in range(1, countCommands):
        countVoiceResponse = len(module[j]["voiceResponse"])
        for k in range(countVoiceResponse):
            if (str.lower(voiceResponse[voiceResponseIterator]) == str.lower(module[j]["voiceResponse"][k])):
                return True
    return False

def ExistNameCommand(data, nameModule, nameCommand):
    countModules = len(data["Modules"])
    for i in range(countModules):
        if (data["Modules"][i][0]["nameModule"] == nameModule):
            if (ExistNameCommandAtModule(i, data, nameCommand)):
                return True
    return False

def ExistVoiceResponse(data, voiceResponse):
    countVoiceResponse = len(voiceResponse)
    for t in range(countVoiceResponse):
            countModules = len(data["Modules"])
            for i in range(countModules):
                module = data["Modules"][i]
                if (ExistVoiceResponseAtModule(t, module, voiceResponse)):
                    return True
    return False

def GetNewDataAfterDelCommand(ModuleIterator, data, currentCommand):
    countCommands = len(data["Modules"][ModuleIterator])
    for j in range(1, countCommands):
        if (data["Modules"][ModuleIterator][j]["name"] == currentCommand):
                data["Modules"][ModuleIterator].pop(j)
                return data

class Editor(object):
    @staticmethod
    def AddEmptyModule(nameModule):
        data = LoadFile("Modules.json")
        countModules = len(data["Modules"])
        for i in range(countModules):
            if (data["Modules"][i][0]["nameModule"] == nameModule):
                return -1

        data["Modules"].append([{"nameModule":nameModule}])
        OverwriteFile("Modules.json", data)

    @staticmethod
    def AddCommand(nameModule, nameCommand, voiceResponse, path):
        data = LoadFile("Modules.json")
        if ExistNameCommand(data, nameModule, nameCommand):
            return -1

        if ExistVoiceResponse(data, voiceResponse):
            return -2

        countModules = len(data["Modules"])
        for i in range(countModules):
            if (data["Modules"][i][0]["nameModule"] == nameModule):
                if (len(voiceResponse) == 0):
                    return -3
                data["Modules"][i].append({"name":nameCommand, "voiceResponse":voiceResponse, "path":path})
                break
        OverwriteFile("Modules.json", data)

    @staticmethod
    def DeleteModule(currentModule):
        data = LoadFile("Modules.json")
        countModules = len(data["Modules"])
        for i in range(countModules):
            if (data["Modules"][i][0]["nameModule"] == currentModule):
                data["Modules"].pop(i)
                break
        OverwriteFile("Modules.json", data)
    
    @staticmethod
    def DeleteCommand(currentModule, currentCommand):
        data = LoadFile("Modules.json")
        countModules = len(data["Modules"])
        for i in range(countModules):
            if (data["Modules"][i][0]["nameModule"] == currentModule):
                data = GetNewDataAfterDelCommand(i, data, currentCommand)
                OverwriteFile("Modules.json", data)
                return 0
        return -1