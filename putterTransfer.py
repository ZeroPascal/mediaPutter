
import subprocess
import platform
from pathlib import Path
import sys
import re
import putterConfig


config = putterConfig.ReadConfig()

def run(cmd):
   
    if(platform.system() == 'Windows'):
        return runWindows(cmd)
    
    return runUnix(cmd)

def runUnix(cmd):
    return str(subprocess.run([cmd],stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True))

def runWindows(cmd):
    return str(subprocess.run(['powershell',cmd],stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True))

def cmdTest():
    #if(platform.system() == 'Windows'):
     #   print(subprocess.run(["powershell","ping", "192.168.1.1"],stdout=subprocess.PIPE))

    #cmd = "echo 'put C:\\Users\\Winst\\Desktop\\frida.aif' | sftp pi@192.168.1.8:Desktop/"
    if(platform.system() == 'Windows'):
        
        cmd = "echo 'ls' | sftp pi@192.168.1.8:Desktop/"
        file = 'test with spaces.txt'
        remoteFiles = runWindows(cmd)
        hasFile = remoteFiles.find(file)>-1
        print(file, ' is on Remote Server? ', hasFile)
        if not hasFile:
            cmd = "scp -v C:\\Users\\Winst\\Desktop\\"+file+" pi@192.168.1.8:Desktop"
            resutls = runWindows(cmd)
            if(resutls.find('Exit status 0')>-1):
                return 'Transfer Successful'
            else:
                return 'Transfer Failed'
        else:
            return 'File Already Exist'

 
        #while True:
        
         #   output = process.stdout
          #  if process.poll() is not None:
           #     print('Done')
            #    break
            #if output != '':
             #   print(str(output))


def Putt(serverList: dict, feedback):
    global config 
    config = putterConfig.ReadConfig()
    feedback('Putting! '+ platform.system())
    #print('File Transfter Successful? ',cmdTest())
    tempFolder = makeDestinationFolder()
    for serverID in serverList:
        feedback(serverID)
        try:
            feedback(sendDestinationFolders(serverID, tempFolder))
            for file in serverList.get(serverID):
                feedback("   ",file)
                sendFile(file,serverID)
        except Exception as e:
            feedback(e)
            
 

    removeDestinationFolder(tempFolder)

def removeDestinationFolder(tempFolder: Path):
    tempFolder.rmdir()

def makeDestinationFolder():
    global config
    configPath = putterConfig.getPutterFolderPath()
    #print(configPath.as_posix())
    
    tempFolder = configPath / config['destinationFolder']
    #print(tempFolder)
    tempFolder.mkdir(parents=True, exist_ok=True)
    return tempFolder

def sendDestinationFolders(serverID, tempFolder: Path):
    global config
    tempPath = tempFolder.as_posix()
    try:
        if (platform.system() == 'Windows'):
            cmd = "scp -rv ConnectTimeout=10 "+tempPath+" "+config['ipSchema']+str(serverID)+":"+config['destinationPath']
            results = run(cmd)
            if(results.find('Exit status 0')>-1):
                return 'Destination Folder Place Successful'
            else:
                print(' ')
        else:
            cmd = "rsync -rP "+tempPath+" "+config['ipSchema']+str(serverID)+":"+config['destinationPath']
    except:
       raise Exception('Malformed Config')   
    
    print(cmd)
    raise Exception('Destination Folder Place Failed')

def sendFile(fileName, serverID):
    global config
    print(config['sourceFolder'])
    file = Path(config['sourceFolder'])
   
    file = file.as_posix()
    try:
        if (platform.system() == 'Windows'):
            cmd = "echo 'ls' | stfp "+config['ipSchema']+str(serverID)+":"+config['destinationPath']+config['destinationFolder']
            remoteFiles = runWindows(cmd)
            hasFile = remoteFiles.find(fileName)>-1
            if not hasFile:
                cmd = "scp -v "+file+" "+config['ipSchema']+str(serverID)+":"+config['destinationPath']+config['destinationFolder']
            else:
                return 'File Already Exist'
        else:
            cmd = "rsync -rP "+file+" "+config['ipSchema']+str(serverID)+":"+config['destinationPath']+config['destinationFolder']
    except:
       raise Exception('Malformed Config')

    print(cmd)
    run(cmd)


    #if(platform.system() == 'Windows'):
        #print(subprocess.run(["powershell","ping", "192.168.1.1"]))
