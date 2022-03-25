from pathlib import Path
import json
from webbrowser import get
defaultConfig = '{"sourceFolder": "", "filter": "", "destinationFolder": "", "serverMediaFolder" : "/Applications/Mbox/Media/"}'
defaults = json.loads(defaultConfig)

currentConfig = defaults

def updateCurrentConfig(newConfig):
    global currentConfig
    currentConfig =newConfig

def getPath():
    configPath = Path(str(Path.home())+"/.mediaPutter")
    configPath.mkdir(parents=True, exist_ok=True)
    #print(configPath)

    filePath = Path(str(configPath)+'/mediaPutter.json')
    if not filePath.is_file():   
        print('No Local File Found, Making One!')
        open(filePath, 'w+').close()

    return filePath

def ReadConfig():
    global defaults
    file = open(getPath(),'r')
    read = file.read()
    try:
        local = json.loads(read)
    except:
        local = json.loads('{}')
    updated = {**local,**defaults}
    for x,y in local.items():
        updated[x] = y

    file.close()
    final = open(getPath(),'w')
    final.write(json.dumps(updated))
    final.close()
    updateCurrentConfig(updated)
    return updated

def UpdateConfig(lineItem, value):
    current = ReadConfig()
    newItem = {lineItem: value}
    updated= { **current, **newItem }
    file = open(getPath(),'w')
    file.write(json.dumps(updated))
    file.close()
    updateCurrentConfig(updated)






