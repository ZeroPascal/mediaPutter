from tkinter import *
from tkinter import tix
from tkinter import filedialog
import threading
from os import listdir
from os.path import isfile, join
from putterConfigPage import update
import putterTransfer
import putterConfig
import re

from putterTransferPage import TransferPage

class MainPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.name= 'MainPage'
        self.controller = controller
        #self.config['sourceFolder'] = ''
        self.mediaFiles = []
        self.selectedMediaFiles = []
        self.serverList = {}
        self.config = putterConfig.ReadConfig()
        #self.config['sourceFolder']= self.initalConfig['sourceFolder']
        mediaList = Listbox(self, width=55, selectmode=EXTENDED, name='mediaList')
        filterString =StringVar()
        filterString.set(putterConfig.getConfig('filter'))
        fileDirectory = tix.HList(self,width=55, height=12)
        configError=Label(self,text="")


       


        

        def updateMediaFolder():
            if not self.config['sourceFolder']:
                return 
        
            mediaList.delete(0,mediaList.size())
            try:
                self.mediaFiles = [f for f in listdir(self.config['sourceFolder']) if isfile(join(self.config['sourceFolder'], f))]
                i=0
                    
                for file in self.mediaFiles:
                    i+=1
                    mediaList.insert(i,file)
            except:
                print('MediaFolder Update Failed: ',self.config['sourceFolder'])
                
            mediaList.update()
            updateFilter(filterString)
            putterConfig.UpdateConfig('sourceFolder',self.config['sourceFolder'])

        def selectMediaFolder():
            try:
                self.config['sourceFolder'] = filedialog.askdirectory()
            except:
                self.config['sourceFolder'] = ''
            if self.config['sourceFolder']:
                updateMediaFolder()

               
        def updateSelectedMedia(evt):
            
            #global selectedMediaFiles

            s = mediaList.curselection()
            self.selectedMediaFiles= []
            for i in s:
                self.selectedMediaFiles.append(mediaList.get(i))
            #print('Selected Media Files:' ,selectedMediaFiles)
            updateFilter(filterString)

        def putterFeedBack(update:str):
            print('Updated: ',update)
            return update

        def hideTransfer():
            print('Hidding Transfer')
            self.show()
        
        def cancelTransfer():
            print('Canceling')
           
            self.show()
        
        def startPutter():
            global row1
            for item, value in putterConfig.ReadConfig().items():
                
                if item == 'destinationFolder' or item == 'destinationPath' or item == 'ipSchema':
                    if not value:
                        print('bad item',item)
                        configError.config(text=item+" Can NOT be blank")
                        return
           
           # transferPage.start(hideTransfer,cancelTransfer)
            #transferPage = TransferPage(self,cancelTransfer,hideTransfer)
            self.controller.startTransfer(self.serverList,self.config)
            #p = threading.Thread(target=putterTransfer.Putt, args=(self.serverList, transferPage.logFeedback))
           # p.start()
            
        def updateFilter(filter):
           
            putterConfig.UpdateConfig('filter',filter.get())
           
            self.serverList = {}
            fileDirectory.delete_all()
            for file in self.mediaFiles:
                #print(file, file+"" in selectedMediaFiles,selectedMediaFiles)
                if file not in self.selectedMediaFiles:
                    try:
                        rex = re.compile(filter.get())
                    except:
                        rex = ''
                    match = re.findall(rex ,file)


                    if match:
                        rex2 = re.compile("\d\d\d")
                        try:
                            serverID = int(re.search(rex2,match[0]).group(0))
                        except:
                            serverID = 0
                            
                        if not self.serverList.get(serverID):
                            self.serverList[serverID] = [file]
                        else:
                            self.serverList[serverID].append(file)

            for server in self.serverList:
                pPath = fileDirectory.add(server, text=server)
                i = 0
                for file in self.serverList.get(server):
                    fileDirectory.add_child(pPath,text=file)
                    i+=1
            #print(serverList)

        updateMediaFolder()
        row1= 10
        Button(self, text="Select Media Folder",command=selectMediaFolder).place(x=10,y=10)

        row2= row1+25
        Label(self,text='Media Files (Select to ignore):').place(x=10,y=row2)
       
        mediaList.bind('<<ListboxSelect>>', updateSelectedMedia)
        mediaList.place(x=10,y=row2+25)

        row3= row2+200
        filterLabel=Label(self,text="Filter:")
        filterLabel.place(x=10,y=row3)
       
        filterString.trace("w", lambda name, index, mode, filterString=filterString: updateFilter(filterString))
        filterEntry = Entry(self, textvariable=filterString)
        filterEntry.place(x=45,y=row3)

        row4= row3+25
        Label(self, text='Media Per Filtered Server:').place(x=10,y=row4)
        fileDirectory.place(x=10, y= row4+25)

        row5= row4+200
        Label(self,text="Destination Folder:").place(x=10, y=row5)

        destinationFolder =StringVar()
        destinationFolder.set(self.config['destinationFolder'])
        destinationFolder.trace("w", lambda name, index, mode, destinationFolder=destinationFolder: putterConfig.UpdateConfig('destinationFolder',destinationFolder.get()))
        destinationFolderEntry = Entry(self, width=40, textvariable=destinationFolder)
        destinationFolderEntry.place(x=120,y=row5)

        row6 = row5+25
        Label(self,text="Destination Path:").place(x=10, y=row6)
        destinationPath =StringVar()
        destinationPath.set(self.config['destinationPath'])
        destinationPath.trace("w", lambda name, index, mode, destinationPath=destinationPath: putterConfig.UpdateConfig('destinationPath',destinationPath.get()))
        destinationPathEntry = Entry(self, width=40, textvariable=destinationPath)
        destinationPathEntry.place(x=120,y=row6)

        row7 = row6+25
        Label(self,text="IP Schema:").place(x=10, y=row7)
        ipSchema =StringVar()
        ipSchema.set(self.config['ipSchema'])
        ipSchema.trace("w", lambda name, index, mode, ipSchema=ipSchema: putterConfig.UpdateConfig('ipSchema', ipSchema.get()))
        ipSchemaEntry = Entry(self, width=40, textvariable=ipSchema)
        ipSchemaEntry.place(x=120,y=row7)

        row8 = row7+50
        
        configError.place(x=15,y=row8-20)
        Button(self, text="Start Transfer",command=startPutter).place(x=150,y=row8)


