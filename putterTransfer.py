
from http import server
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
    def __init__(self, serverList: dict, config:dict, feedback,stopThread):
        
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

    def getDest(self,includeDestinationFolder= True):
        
        if(self.config['ipSchema']):
            dest = self.config['ipSchema']+":"+self.config['destinationPath']
        else:
            dest = self.config['destinationPath']

        if(includeDestinationFolder):
            dest+=self.config['destinationFolder']

        return dest

    def start(self):
        self.stopPoll =threading.Thread(target=checkStop,args=(self.stopThread,self.getProcesses,self.stop,))
        self.stopPoll.start()
        
        
        for serverID in self.serverList:
                    if(self.stopThread()):
                        print('Got Stop in Server Loop',serverID)
                        break
                    tempFolder = self.makeDestinationFolder(serverID)
                    self.feedback(serverID, None, 'Starting')
                    try:
                        self.feedback(serverID, None, self.sendDestinationFolders(serverID, tempFolder))
                        self.feedback(serverID, None,'Sending Files to Server')
                        for file in self.serverList.get(serverID):
                                print("File",file)
                                self.fileQueue.append({serverID:file})
                                self.feedback(serverID,file, 'Starting')
                                fileFeedback = self.sendFile(file,serverID)
                                self.feedback(serverID, file, fileFeedback )
                                self.fileQueue.remove({serverID:file})

                    except Exception as e:
                            self.feedback(serverID,None,  e)
                    try:
                        self.removeDestinationFolder(tempFolder)
                    except:
                        print('Can Not Remove Temp Folder')
            

        if (self.stopFlag):
            self.feedback(None,None,'Transfer Stopped')
            print('Transfer Thread Alive?',self.stopPoll.is_alive())
        if not self.processes:
            time.sleep(1)
            self.feedback(None,None,'Done!')
            self.stopThread(True)

    def run(self,cmd:str):
        #Cleans Wildcards
        cmd = cmd.replace('*','')
        try:
            print('Job Starting',cmd)
            if(platform.system() == 'Windows'):
                p= self.runWindows(cmd)
            else:
                p = self.runUnix(cmd)
            self.processes.append(p)
            out = p.communicate()
            if not p.poll() or out[1]:
                self.processes.remove(p)
                print('Job done',cmd)
            
            return out[0]+out[1]
        except:
            print('Run Got Error',p, self.processes)
            p.terminate()
            try:
                self.processes.remove(p)
            except:
                None

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

    def replaceIDWildCard(self,cmd:str, serverID:int):
        return cmd.replace('$ID',str(serverID))

    def makeDestinationFolder(self,serverID):
    
        configPath = putterConfig.getPutterFolderPath()
        #print(configPath.as_posix())
        dest = self.replaceIDWildCard(self.config.get('destinationFolder'),serverID)
        
        tempFolder = configPath / dest

        print(tempFolder)
        tempFolder.mkdir(parents=True, exist_ok=True)
        return tempFolder

    def sendDestinationFolders(self,serverID, tempFolder: Path):
        #print(self.config)
        tempPath = tempFolder.as_posix()
        try:
            
            cmd:str = "scp -rv "+tempPath+" "+self.getDest(False)
            cmd = self.replaceIDWildCard(cmd,serverID)
            results = self.run(cmd)
            if 'Exit status 0' in results:
                return 'Successfully placed Destination Folder'
            elif 'user (unspecified)' in results:
                raise Exception('Invalid User')
            elif 'lost connection' in results:
                raise Exception('Could Not Connect To Client')
                
        except Exception as e:
            print(e)
            raise e   
        
        #print(cmd)
        raise Exception('Failed to place Destination Folder')


    def deleteFile(self, serverID, fileName):
        cmd:str = "echo 'rm "+fileName+"' | sftp "+self.getDest()
        cmd = self.replaceIDWildCard(cmd,serverID)
        self.run(cmd)

    def sendFile(self,fileName, serverID):
        print('Sending File!',fileName, 'to',serverID)
        
        file = Path(self.config['sourceFolder'])
        file = file / fileName
        file = file.as_posix()
        try:
          
            cmd:str = "echo 'ls' | sftp "+self.getDest()
            cmd = self.replaceIDWildCard(cmd,serverID)
            remoteFiles = self.run(cmd)
            hasFile = remoteFiles.find(fileName)>-1
            if not hasFile:
                cmd = "scp -v "+file+" "+self.getDest()
            else:
                return 'File Already Exist'
    
        except Exception as e:
            raise Exception('Malformed Config',e)
        cmd = self.replaceIDWildCard(cmd,serverID)
        result = self.run(cmd)
        if(result.index('Exit status 0')>-1):
            return 'Complete'
        return 'Failed'


    #if(platform.system() == 'Windows'):
        #print(subprocess.run(["powershell","ping", "192.168.1.1"]))
