
import signal
import os
import subprocess
import platform
from pathlib import Path
import threading
import time
import putterConfig

            
def checkStop(stopThread, processes, stop):
    while not stopThread():
        time.sleep(.5)
    print('CheckStop Sending Stop!')
    #print(processes())
    stop(processes())
    raise SystemExit()
        

class Putt():
    def __init__(self, serverList: dict, config, feedback,stopThread):
        
            self.processes = []
            self.fileQueue =[]
            self.config = config
           # print(self.config)
            self.serverList= serverList
            self.stopThread = stopThread
            self.feedback = feedback
            self.stopFlag = False
            feedback(None,None,'Putting!')
            self.start()
            

    def stop(self,processes):
        self.stopFlag = True
        
        for p in processes:
            
            p.terminate()

        for tupple in self.fileQueue:
            for server, file in tupple.items():
            
                self.deleteFile(server,file)

        raise SystemExit()

    def getProcesses(self):
        return self.processes

    def start(self):
        self.stopPoll =threading.Thread(target=checkStop,args=(self.stopThread,self.getProcesses,self.stop,))
        self.stopPoll.start()
        
        tempFolder = self.makeDestinationFolder()
        for serverID in self.serverList:
                    if(self.stopThread()):
                        print('Got Stop in Server Loop',serverID)
                        break
                    self.feedback(serverID, None, 'Starting')
                    #try:
                    self.feedback(serverID, None, self.sendDestinationFolders(serverID, tempFolder))
                        #print('Stop?',self.stopThread())
                    self.feedback(serverID, None,'Sending Files to Server')
                    for file in self.serverList.get(serverID):
                            print("File",file)
                            self.fileQueue.append({serverID:file})
                            self.feedback(serverID,file, 'Starting')
                            fileFeedback = self.sendFile(file,serverID)
                            self.feedback(serverID, file, fileFeedback )
                            self.feedback(serverID, None, 'Complete') 
                            self.fileQueue.remove({serverID:file})

                    #except Exception as e:
                     #       self.feedback(serverID,None,  e)

        self.removeDestinationFolder(tempFolder)
            

        if (self.stopFlag):
            self.feedback(None,None,'Transfer Stopped')
            print('Transfer Thread Alive?',self.stopPoll.is_alive())
        elif not self.processes:
            time.sleep(1)
            self.feedback(None,None,'Done!')
            self.stopThread(True)

    def run(self,cmd):
        print('Job Starting',cmd)
        if(platform.system() == 'Windows'):
            p= self.runWindows(cmd)
        else:
            p = self.runUnix(cmd)
        self.processes.append(p)
        out = p.communicate()
        if not p.poll():
            self.processes.remove(p)
            print('Job done',cmd)
        
        return out[0]+out[1]


    def runUnix(self,cmd):
        return subprocess.Popen([cmd],stdout=subprocess.PIPE,stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)

    def runWindows(self,cmd):
        return subprocess.Popen(['powershell',cmd],stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True, shell=True)

    def cmdTest(self):
        #if(platform.system() == 'Windows'):
        #   print(subprocess.run(["powershell","ping", "192.168.1.1"],stdout=subprocess.PIPE))

        #cmd = "echo 'put C:\\Users\\Winst\\Desktop\\frida.aif' | sftp pi@192.168.1.8:Desktop/"
        if(platform.system() == 'Windows'):
            
            cmd = "echo 'ls' | sftp pi@192.168.1.8:Desktop/"
            file = 'test with spaces.txt'
            remoteFiles = self.runWindows(cmd)
            hasFile = remoteFiles.find(file)>-1
            print(file, ' is on Remote Server? ', hasFile)
            if not hasFile:
                cmd = "scp -v C:\\Users\\Winst\\Desktop\\"+file+" pi@192.168.1.8:Desktop"
                results = self.runWindows(cmd)
                if(results.find('Exit status 0')>-1):
               # if(results == 0):
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




    def removeDestinationFolder(self, tempFolder: Path):
        tempFolder.rmdir()

    def makeDestinationFolder(self):
    
        configPath = putterConfig.getPutterFolderPath()
        #print(configPath.as_posix())
        
        tempFolder = configPath / self.config['destinationFolder']
        #print(tempFolder)
        tempFolder.mkdir(parents=True, exist_ok=True)
        return tempFolder

    def sendDestinationFolders(self,serverID, tempFolder: Path):
        #print(self.config)
        tempPath = tempFolder.as_posix()
        try:
            
            cmd = "scp -rv "+tempPath+" "+self.config['ipSchema']+str(serverID)+":"+self.config['destinationPath']
            results = self.run(cmd)
            if(results.find('Exit status 0')>-1):
                return 'Successfully placed Destination Folder'
                
        except Exception as e:
            raise Exception('Malformed Config',e)   
        
        #print(cmd)
        raise Exception('Failed to place Destination Folder')
    def deleteFile(self, serverID, fileName):
        cmd = "echo 'rm "+fileName+"' | sftp "+self.config['ipSchema']+str(serverID)+":"+self.config['destinationPath']+self.config['destinationFolder']
        self.run(cmd)
    def sendFile(self,fileName, serverID):
        print('Sending File!',fileName, 'to',serverID)
        print('SourceFolder',self.config['sourceFolder'])
        file = Path(self.config['sourceFolder'])
        file = file / fileName
        file = file.as_posix()
        try:
        
            cmd = "echo 'ls' | sftp "+self.config['ipSchema']+str(serverID)+":"+self.config['destinationPath']+self.config['destinationFolder']
            remoteFiles = self.run(cmd)
            print(remoteFiles)
            hasFile = remoteFiles.find(fileName)>-1
            if not hasFile:
                cmd = "scp -v "+file+" "+self.config['ipSchema']+str(serverID)+":"+self.config['destinationPath']+self.config['destinationFolder']
            else:
                return 'File Already Exist'
    
        except Exception as e:
            raise Exception('Malformed Config',e)

        print(cmd)
        result = self.run(cmd)
        if(result.index('Exit status 0')>-1):
            return 'Complete'
        return 'Failed'


    #if(platform.system() == 'Windows'):
        #print(subprocess.run(["powershell","ping", "192.168.1.1"]))
