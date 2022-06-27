def ExistSubstring(substring, string):
    substring = str.lower(substring)
    string = str.lower(string)
    substringLength = len(substring)
    stringLength = len(string)

    if (substring == string):
        return True
    if (substringLength >= stringLength):
        return False

    for i in range(stringLength - substringLength + 1):
        sum = 0
        for j in range(substringLength):
            if (substring[j] != string[i + j]):
                break
            
            sum += 1
            if (sum == substringLength):
                return True
    return False


def SearchModule(substring, modulelist):
    modules = []
    countModules = len(modulelist.modules)
    for i in range(countModules):
        if(ExistSubstring(substring, modulelist.modules[i].name)):
            modules.append(modulelist.modules[i].name)
    return modules

def SearchCommand(substring, moduleList , currentNameModule):
    commands = []
    countModules = len(moduleList.modules)
    for i in range(countModules):
        module = moduleList.modules[i]
        if(module.name == currentNameModule):
            countCommands = len(module.commands)
            for j in range(countCommands):
                if(ExistSubstring(substring, moduleList.modules[i].commands[j].name)):
                    commands.append(moduleList.modules[i].commands[j].name)
            break
    return commands

def SearchModulesAndCommands(substring, moduleList, currentNameModule):
    ModulesAndCommands = []
    ModulesAndCommands.append({"Modules": SearchModule(substring, moduleList)})
    ModulesAndCommands.append({"Commands": SearchCommand(substring, moduleList, currentNameModule)})
    return ModulesAndCommands