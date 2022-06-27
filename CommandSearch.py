from fuzzywuzzy import fuzz
from ConnectingModule import *

def findCommand(voiceResponse, modulelist):
    countModules = len(modulelist.modules)
    max = 0
    count = 0
    for i in range(countModules):
        module = modulelist.modules[i]
        countCommands = len(module.commands)
        for j in range(countCommands):
            countVoiceResponse = len(module.commands[j].voiceResponse)
            for k in range(countVoiceResponse):
                resultСomparison = fuzz.WRatio(voiceResponse, module.commands[j].voiceResponse[k])
                if (resultСomparison > max):
                    max = resultСomparison
                    count = 1
                    result = module.commands[j]
                elif (resultСomparison == max):
                    count += 1
    if (max > 90 and count == 1):
        return result
    return None

def findInternalCommand(voiceResponse, internalModuleList):
    countCommands = len(internalModuleList.commands)
    max = 0
    count = 0
    for j in range(countCommands):
        countVoiceResponse = len(internalModuleList.commands[j].voiceResponse)
        for k in range(countVoiceResponse):
            resultСomparison = fuzz.WRatio(voiceResponse, internalModuleList.commands[j].voiceResponse[k])
            if (resultСomparison > max):
                max = resultСomparison
                count = 1
                result = internalModuleList.commands[j]
            elif (resultСomparison == max):
                count += 1
    if (max > 90 and count == 1):
        return result
    return None

def commandSearch(voiceResponse, modulelist):
    list = voiceResponse.split()
    list2 = []
    if voiceResponse != "":
        for i in range(1, len(list) + 1):
            string = ""
            for j in range(i):
                string = string + " " + list[j]
            list2.append(string[1:])

    for item in list2:
        result = findCommand(item, modulelist)
        if result != None:
            return result

    return None

def internalCommandSearch(voiceResponse, internalModuleList):
    list = voiceResponse.split()
    list2 = []
    if voiceResponse != "":
        for i in range(1, len(list) + 1):
            string = ""
            for j in range(i):
                string = string + " " + list[j]
            list2.append(string[1:])

    for item in list2:
        result = findInternalCommand(item, internalModuleList)
        if result != None:
            return result

    return None