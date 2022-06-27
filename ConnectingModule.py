import json
from Interface import *
from TextProcessing import *

class ModuleList(object):
    def __init__(self):
        self.modules = []
        """Constructor"""
        with open("Modules.json", "r",  encoding='utf-8') as read_file:
            data = json.load(read_file)
        modules = data["Modules"]
        count = len(modules)
        for i in range(count):
            self.modules.append(Module(modules[i]))


class Module(object):
    def __init__(self, module):
        """Constructor"""
        self.name = module[0]["nameModule"]
        self.commands = []
        count = len(module)
        for i in range(1, count):
            self.commands.append(Command(module[i]["path"], module[i]["voiceResponse"], module[i]["name"]))


class Command(object):
    def __init__(self, path, voiceResponse, name):
        """Constructor"""
        self.path = path
        self.voiceResponse = voiceResponse
        self.name = name


class InternalCommand(object):
    def __init__(self, func, voiceResponse):
        """Constructor"""
        self.func = func
        self.voiceResponse = voiceResponse


class InternalModuleList:
    def __init__(self, openWindow, closeWindow, stopListening):
        self.commands = []
        """Constructor"""
        self.commands.append(InternalCommand(openWindow, ["открой программу", "откройся", "открой интерфейс", "покажись"]))
        self.commands.append(InternalCommand(closeWindow, ["закрой программу", "закройся", "закрой интерфейс", "спрячься"]))
        self.commands.append(InternalCommand(stopListening, ["выключись", "замолкни", "хватит слушать", "остановись"]))