from itertools import count
import json
import datetime

class Commands:
    def __init__(self, voiceCommand, needStatic=None):
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.nameCommand = voiceCommand
        if(needStatic == True):
            self.countRepetitions = 1

def checkFileHistory():
    try:
        f = open('history.json')
        f.close()
    except FileNotFoundError:
        data = {"SaveHistoryCommands":[]}
        data = json.dumps(data)
        data = json.loads(str(data))
        with open("history.json", 'w', encoding ='utf-8') as file:
            json.dump(data, file, sort_keys=False, indent = 2, ensure_ascii=False, separators=(',', ': '))

def checkFileUnrecognizedСommands():
    try:
        f = open("unrecognizedСommands.json")
        f.close()
    except FileNotFoundError:
        data = {"SaveHistoryUnrecognizedСommands":[]}
        data = json.dumps(data)
        data = json.loads(str(data))
        with open("unrecognizedСommands.json", 'w', encoding = 'utf-8') as file:
            json.dump(data, file, sort_keys=False, indent = 2, ensure_ascii=False, separators=(',', ': '))

def write(data, filename):
    data = json.dumps(data)
    data = json.loads(str(data))
    with open(filename, 'w', encoding = 'utf-8') as file:
        json.dump(data, file, sort_keys=False, indent = 2, ensure_ascii=False, separators=(',', ': '))

def read(filename):
    with open(filename, 'r', encoding = 'utf-8') as file:
        return json.load(file)

def findVoiceResponse(data, voiceResponse):
    countVoiceResponses = len(data["SaveHistoryUnrecognizedСommands"])
    for i in range(countVoiceResponses):
        if(data["SaveHistoryUnrecognizedСommands"][i]["nameCommand"] == voiceResponse):
            return i
    return None

def recordHistory(filename, voiceCommand):
    if (filename == "history.json"):
        checkFileHistory()
        data = read(filename)
        data["SaveHistoryCommands"].append(Commands(voiceCommand).__dict__)
        write(data, filename)
    else:
        checkFileUnrecognizedСommands()
        data = read(filename)
        number = findVoiceResponse(data, voiceCommand)
        if(number != None):
            data["SaveHistoryUnrecognizedСommands"][number]["date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data["SaveHistoryUnrecognizedСommands"][number]["countRepetitions"] += 1
        else:
            data['SaveHistoryUnrecognizedСommands'].append(Commands(voiceCommand, True).__dict__)
        write(data, filename)

def chronologicallyFilter(data, typeHistory):
    return sorted(data[typeHistory], key=lambda n: n["date"], reverse=True)

def statisticalFilter(data, typeHistory):
    if(typeHistory != "SaveHistoryCommands"):
        return sorted(data[typeHistory], key=lambda n: n["countRepetitions"], reverse=True)
    else:
        historyCommands = []
        countCommands = len(data[typeHistory])
        for i in range(countCommands):
            historyCommands.append(data[typeHistory][i])
        return historyCommands

def converterHistoryList(data):
    historyList = []
    countCommands = len(data)
    for i in range(countCommands):
        if(len(data[i]) == 2):
            historyList.append(str(data[i]["date"].replace("-",".")) + " " + data[i]["nameCommand"])
        else:
            historyList.append(str(data[i]["date"].replace("-",".")) + " " + data[i]["nameCommand"]
            + " - "+ str(data[i]["countRepetitions"]))
    return historyList

def updateHistory(mainWindow):
    typeHistory = ""
    if(mainWindow.recognizeNumber == 1):
        typeHistory = "SaveHistoryCommands"
        data = read("history.json")
        if(mainWindow.chronologicallyNumber == 0):
            data = chronologicallyFilter(data, typeHistory)
        else:
            data = statisticalFilter(data, typeHistory)
    else:
        data = read("unrecognizedСommands.json")
        typeHistory = "SaveHistoryUnrecognizedСommands"
        if(mainWindow.recognizeNumber == 2):
            if(mainWindow.chronologicallyNumber == 0):
                data = chronologicallyFilter(data, typeHistory)
            else:
                data = statisticalFilter(data, typeHistory)
        elif(mainWindow.chronologicallyNumber == 0):
            dataHistory = read("history.json")
            data[typeHistory].extend(dataHistory["SaveHistoryCommands"])
            data = chronologicallyFilter(data, typeHistory)
        else:
            data = statisticalFilter(data, typeHistory)
            dataHistory = read("history.json")
            data.extend(dataHistory["SaveHistoryCommands"])


    mainWindow.clearHistoryList()
    capacityHistoryList = 0
    if(mainWindow.amountNumber == 0):
        capacityHistoryList = 10
    elif(mainWindow.amountNumber == 1):
        capacityHistoryList = 25
    elif(mainWindow.amountNumber == 2):
        capacityHistoryList = 50
    else:
        capacityHistoryList = 100
    
    countCommands = len(data)
    if(countCommands > capacityHistoryList):
        for i in range(countCommands - capacityHistoryList):
            data.pop()
    mainWindow.addItemsInHistoryList(converterHistoryList(data))