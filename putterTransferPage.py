import threading
#import multiprocessing
from tkinter import *
from tkinter.ttk import Treeview
import putterTransfer

class TransferPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.name= 'TransferPage'
        self.controller = controller
        self.serverList = {}
        self.stopTransfer = False
        Label(self,text='Transfer updateBoard').place(x=10, y=10)
        self.updateBoard=Listbox(self,width=55,selectmode=EXTENDED,name='updateBoard')
        self.updateBoard.place(x=10,y=30)
       # self.cancelCallback = cancel
        #self.hideCallback = hide
        self.updateBoardFeedback = ()
        self.log = Listbox(self, width=55, selectmode=EXTENDED, name='log')

        self.logSize=0
        self.serverMessageList = {}
        self.fileMessageList ={}
       # log.bind('<<ListboxSelect>>', updateLog)
        self.log.place(x=10,y=250)


        def cancelTransfer():
           print('Cancel')
           self.stopTransfer = True
           self.controller.quitTransfer()
           
        self.cancelString= StringVar()
        self.cancelString.set('Cancel')

        self.cancelButton = Button(self,textvariable=self.cancelString,command=cancelTransfer)
        self.cancelButton.place(x=10,y=450)

    def stopThread(self,stop=False):
        if stop:
            self.stopTransfer = stop

        if  self.stopTransfer:
            #print('Stop Thread Triggered',self.stopTransfer,stop)
            self.cancelString.set('Exit')

        return self.stopTransfer



    def feedback(self, serverID = None, fileName = None, message=None):
        #print(serverID,fileName,message)
        if not fileName and not serverID and not message:
            self.log.insert(self.logSize,'')
        elif not fileName and not serverID:
              self.log.insert(self.logSize,str(message))
        elif not serverID and not fileName:
          
            self.log.insert(self.logSize,":"+str(message))
        
        elif not fileName:
             self.serverMessageList[serverID] = str(message)
             self.log.insert(self.logSize,str(serverID)+":"+str(message))
        else:
            
            
            self.log.insert(self.logSize,str(serverID)+'@'+str(fileName)+" : "+str(message))
            if not self.fileMessageList.get(serverID):
                l = {fileName:message}
                self.fileMessageList.update({serverID:l})
            else:
                fileDict = self.fileMessageList.get(serverID)                
                fileDict.update({fileName:message})

                self.fileMessageList.update({serverID: fileDict})
            #print(self.fileMessageList)
        
   
        self.logSize+=1
        self.redrawBoard()

    def redrawBoard(self):
        #print('Redrawing Board')
        self.updateBoard.delete(0,self.updateBoard.size())
        #self.updateBoard.delete_all()
        i=0
        for server in sorted (self.serverList):
            if server in self.serverMessageList.keys():
                sMSG = self.serverMessageList[server]
                #print('ServerMessage',server,sMSG)
            else:
                sMSG = ''
            self.updateBoard.insert(i, str(server)+' '+sMSG)
            
            if('Starting' in sMSG or 'Successfully' in sMSG or 'Sending Files' in sMSG):
                self.updateBoard.itemconfig(i,{'bg':'yellow','fg':'black'})
            elif('Complete' in sMSG):
                self.updateBoard.itemconfig(i,{'bg':'green'})
            elif (sMSG !=''):
               self.updateBoard.itemconfig(i,{'fg':'red'})

            i+= 1
            for file in self.serverList.get(server):
                if server in self.fileMessageList.keys() and file in self.fileMessageList[server].keys():
                    message= self.fileMessageList[server][file]
                else:
                    message = ''
                self.updateBoard.insert(i,'      '+file+' '+message)
                if('Starting' in message):
                    self.updateBoard.itemconfig(i,{'bg':'yellow','fg':'black'})  
                elif('Already Exist' in message):
                    self.updateBoard.itemconfig(i,{'bg':'orange'})  
                elif('Complete' in message):
                    self.updateBoard.itemconfig(i,{'fg':'green'}) 
                elif(sMSG != '' and not ('Starting'in sMSG or 'Complete' in sMSG or 'Sending Files' in sMSG)) :
                    self.updateBoard.itemconfig(i,{'fg':'red'})
                i+=1
        

    def start(self, serverList,config):
        self.serverList = serverList
        self.fileMessageList ={}
        self.serverMessageList ={}
        self.config = config
       
        #putt = putterTransfer.Putt(self.serverList,self.config,self.feedback)
        self.stopTransfer = False
        self.putt = threading.Thread(target=putterTransfer.Putt, args=(self.serverList,self.config,self.feedback,self.stopThread,))
        self.putt.start()
        
        #putt = Putt(self.serverList,self.config,self.feedback)
        self.redrawBoard()
        self.log.delete(0,self.logSize)
        self.logSize = 0
       

      

    
     

        
       