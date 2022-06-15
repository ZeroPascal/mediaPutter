
from datetime import datetime
import subprocess
import platform
from pathlib import Path
import threading
import time
import putterConfig

            
def checkStop(stopThread, processes, stop):
    while not stopThread():
        time.sleep(.5)
   # print('CheckStop Sending Stop!')
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

    def cleanPath(self,path:str):
        # 
        return '"\''+path+'\'"'
    
    def escapeSpaces(self, string: str):
        return string.replace(' ','\ ')

    def getDest(self, escapeSpaces:bool, includeDestinationFolder= True):
        dest = self.config['destinationPath'] 
        if(includeDestinationFolder):
            dest+= self.config['destinationFolder']+"/"
        if escapeSpaces:
            dest = self.escapeSpaces(dest)
        if(self.config['ipSchema']):
            if not escapeSpaces:
                dest = self.config['ipSchema']+":"+'"\''+dest+'\'"'
            else:
                dest = self.config['ipSchema']+":"+dest
            
        return dest

    def start(self):
        startTime = datetime.now()
        self.stopPoll =threading.Thread(target=checkStop,args=(self.stopThread,self.getProcesses,self.stop,))
        self.stopPoll.start()
        
        
        for serverID in sorted (self.serverList.keys()):
                    if(self.stopThread()):
                        print('Got Stop in Server Loop',serverID)
                        break
                   # tempFolder = self.makeDestinationFolder(serverID)
                    tempFolder = self.replaceIDWildCard(self.config.get('destinationFolder'),serverID)
                    self.feedback(serverID, None, 'Starting')
                    try:
                        self.feedback(serverID, None, self.sendDestinationFolders(serverID, tempFolder))
                        self.feedback(serverID, None,'Sending Files to Server')
                        for file in self.serverList.get(serverID):
                                #print("File",file)
                                self.fileQueue.append({serverID:file})
                                self.feedback(serverID,file, 'Starting')
                                fileFeedback = self.sendFile(file,serverID)
                                self.feedback(serverID, file, fileFeedback )
                                self.fileQueue.remove({serverID:file})
                        self.feedback(serverID,None,'Complete')

                    except Exception as e:
                            print('Main Loop Error',e)
                            if(e!='File Already Exist'):
                                self.feedback(serverID,None,  e)
                    
                   # try:
                   #     self.removeDestinationFolder(tempFolder)
                   # except:
                    #    print('Can Not Remove Temp Folder')
            

        if (self.stopFlag):
            self.feedback(None,None,'Transfer Stopped')
           # print('Transfer Thread Alive?',self.stopPoll.is_alive())
        if not self.processes:
            time.sleep(1)
            totalTime =  datetime.now() -startTime
            
            self.feedback(None,None,str(totalTime))
            self.feedback(None,None,'Done!')
            self.stopThread(True)

    def run(self,cmd:str):
        #Cleans Wildcards
        cmd = cmd.replace('*','')
        #print(cmd)
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
                print('     Job done',cmd)
            
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
        return subprocess.Popen([cmd],stdout=subprocess.PIPE,stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True,shell=True)

    def runWindows(self,cmd):
        return subprocess.Popen(['powershell',cmd],stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True, shell=True)

    def removeDestinationFolder(self, tempFolder: Path):
        tempFolder.rmdir()

    def replaceIDWildCard(self,cmd:str, serverID:int):
        return cmd.replace('$ID',str(serverID))

    def makeDestinationFolder(self,serverID):
    
        configPath = putterConfig.getPutterFolderPath()

        dest = self.replaceIDWildCard(self.config.get('destinationFolder'),serverID)
        
        tempFolder = configPath / dest

        tempFolder.mkdir(parents=True, exist_ok=True)
        return tempFolder
    def sendDestinationFolders(self,serverID,tempFolder:str):
        print(serverID,tempFolder)
        try:
            cmd:str = "echo 'mkdir "+tempFolder+"' | sftp "+self.getDest(True,False)
            if(self.config['useNAS'] == 1):
                cmd = "echo '"+cmd+"' | ssh "+self.config['nasUser']
            cmd = self.replaceIDWildCard(cmd,serverID)
            results = self.run(cmd)
            print(results)
        except Exception as e:
            print('sendDest Error',e)

    def _sendDestinationFolders(self,serverID, tempFolder: Path):
        #print(self.config)
        tempPath = tempFolder.as_posix()
        tempPath = "'"+tempPath+"'" #self.cleanPath(tempPath)
        print('Temp Path: ',tempPath)
        try:
            
            cmd:str = "scp -rv "+tempPath+" "+self.getDest(True,False)
            cmd = self.replaceIDWildCard(cmd,serverID)
            results = self.run(cmd)
            if 'Exit status 0' in results:
                return 'Successfully placed Destination Folder'
            elif 'user (unspecified)' in results:
                raise Exception('Invalid User')
            elif 'lost connection' in results:
                raise Exception('Could Not Connect To Client')
            elif 'ambiguous target' in results:
                raise Exception('Malformed Target')
                
        except Exception as e:
            print('sendDest Error',e)
            raise e   
        
        #print(cmd)
        #raise Exception('Failed to place Destination Folder')


    def deleteFile(self, serverID, fileName):
        cmd:str = "echo 'rm "+self.escapeSpaces(fileName)+"' | sftp "+self.getDest(True)
        cmd = self.replaceIDWildCard(cmd,serverID)
        self.run(cmd)

    def sendFile(self,fileName, serverID):
       # print('Sending File!',fileName, 'to',serverID)
        if(self.config['useNAS'] == 1):
            file = self.config['nasUser']+':'+'"\''+self.config['nasFolder']+'/'+fileName+'\'"'
        else:
            file = Path(self.config['sourceFolder'])
            file = file / fileName
            file = file.as_posix()
            file = "'"+file+"'" #self.cleanPath(file)
        try:
            if(self.config['overwriteFiles'] == 0):
                cmd:str = "echo 'ls' | sftp "+self.getDest(True)
                cmd = self.replaceIDWildCard(cmd,serverID)
                remoteFiles = self.run(cmd)
                hasFile = remoteFiles.find(fileName)>-1
                if hasFile:
                     return 'File Already Exist'
            
            cmd = "scp -v "+file+" "+self.getDest(True)       
    
        except Exception as e:
            raise Exception('Malformed Config',e)
        cmd = self.replaceIDWildCard(cmd,serverID)
        result = self.run(cmd)
        if(result.index('Exit status 0')>-1):
            return 'Complete'
        return 'Failed'


    #if(platform.system() == 'Windows'):
        #print(subprocess.run(["powershell","ping", "192.168.1.1"]))
