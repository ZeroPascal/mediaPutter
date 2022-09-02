from copyreg import constructor
import platform
from sre_compile import isstring
from tkinter import *
from tkinter import tix
from tkinter import filedialog
from os import listdir
from os.path import isfile, join
from tkinter.ttk import Treeview
from nasScanner import nasScanner
from putterConfigPage import update
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
        if(platform.system() == 'Windows'):
             listWidth = 65
        else:
            listWidth = 50    
        mediaList = Listbox(self, width=listWidth, selectmode=EXTENDED, name='mediaList')
        filterString =StringVar()
        filterString.set(self.config.get('filter'))
        idSizeString = StringVar()
        idSizeString.set(putterConfig.getConfig('idSize'))
        idMod =StringVar()
        idMod.set(self.config.get('idMod'))
        fileDirectory = Listbox(self,width=listWidth,selectmode=EXTENDED,name='fileDirectory')
        overwriteFiles = IntVar()
        overwriteFiles.set(self.config.get('overwriteFiles'))
        useNAS = IntVar()
        useNAS.set(self.config.get('useNAS'))
        configError=Label(self,text="")
        destinationFolder =StringVar()
        destinationFolder.set(self.config.get('destinationFolder'))
        destinationPath =StringVar()
        destinationPath.set(self.config.get('destinationPath'))
        ipSchema =StringVar()
        ipSchema.set(self.config.get('ipSchema'))
        concurrency=StringVar()
        concurrency.set(self.config.get('concurrency'))


        def updateMediaFolder():
            
            if self.config.get('useNAS'):
                self.mediaFiles = nasScanner(self.config.get('nasUser'),self.config.get('nasPath'),self.config.get('nasFolder'))

            elif not self.config.get('sourceFolder'):
                return 
            
            else:
                self.mediaFiles =  [f for f in listdir(self.config.get('sourceFolder')) if isfile(join(self.config.get('sourceFolder'), f))]
                
        
            mediaList.delete(0,mediaList.size())
            try:
                
                i=0
                for file in self.mediaFiles:
                    i+=1
                    mediaList.insert(i,file)
            except:
                print('MediaFolder Update Failed: ',self.config.get('sourceFolder'))
                
            mediaList.update()
            updateFilter(filterString.get())

        def selectMediaFolder():
            try:
                self.config = putterConfig.UpdateConfig('sourceFolder',filedialog.askdirectory())
            except:
                self.config = putterConfig.UpdateConfig('sourceFolder','')
                
            if self.config.get('sourceFolder'):
                updateMediaFolder()
        def selectNASLocation():
            self.controller.nasSelection()
            updateMediaFolder()
               
        def updateSelectedMedia(evt):
            
            #global selectedMediaFiles

            s = mediaList.curselection()
            self.selectedMediaFiles= []
            for i in s:
                self.selectedMediaFiles.append(mediaList.get(i))
           # print('Selected Media Files:' ,self.selectedMediaFiles)
            updateFilter(filterString.get())

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
            if(configError.cget("text")):
                print(configError.cget('text'))
                return 
            for item, value in putterConfig.ReadConfig().items():
                
                if item == 'destinationFolder' or item == 'destinationPath' or item == 'ipSchema':
                    if not value:
                        print('bad item',item)
                        configError.config(text=item+" Can NOT be blank")
                        return
                    else:
                        configError.config(text='')
   
            self.controller.startTransfer(self.serverList,self.config)
        
        def setUseNAS():
            self.config = putterConfig.UpdateConfig('useNAS',useNAS.get())
            updateMediaFolder()

        def setOverWrite():
            self.config = putterConfig.UpdateConfig('overwriteFiles',overwriteFiles.get())

        def updateIDSize(idSizeString:str):

            self.config =putterConfig.UpdateConfig('idSize',idSizeString.strip())   
            updateFilter(filterString.get())

        def updateIDMod(idModString:str):
            self.config = putterConfig.UpdateConfig('idMod',idModString.strip())
            updateFilter(filterString.get())

        def updateFilter(filter):
            self.config =putterConfig.UpdateConfig('filter',filter)
            self.serverList = {}
            idMod = self.config.get('idMod')
            fileDirectory.delete(0,fileDirectory.size())

            for file in self.mediaFiles:
              
                if file not in self.selectedMediaFiles:
                    try:
                        rex = re.compile(self.config.get('filter'))
                    except:
                        rex = ''
                    match = re.findall(rex ,file)

                    if match:
                        id =''
                        for i in range(self.config.get('idSize')):
                            id+='\d'
                          
                        rex2 = re.compile(id)
                        
                        try:
                            serverID = int(re.search(rex2,match[0]).group(0))+idMod
                        except:
                            serverID = 0+idMod
                       # print(serverID, file)
                        if not self.serverList.get(serverID):
                            self.serverList[serverID] = [file]
                        else:
                            self.serverList[serverID].append(file)
            i =0 
            for server in sorted (self.serverList.keys()):
                fileDirectory.insert(i,server)
                i+=1
                for file in sorted (self.serverList.get(server)):
                    #id:str = str(pID)+'@'+str(i)
                    fileDirectory.insert(i,"    "+file)
                    i+=1
                i+=1
            #print(self.serverList)

        updateMediaFolder()
        row1= 10
        Button(self, text="Select Media Folder",command=selectMediaFolder).place(x=10,y=10)
        Button(self, text="NAS Location",command=selectNASLocation).place(x=170,y=10)
        Checkbutton(self,text='use NAS',variable=useNAS,onvalue=1,offvalue=0,command=setUseNAS).place(x=300,y=(row1+5))
        row2= row1+27
        Label(self,text='Media Files (Select to ignore):').place(x=10,y=row2)


       
        mediaList.bind('<<ListboxSelect>>', updateSelectedMedia)
        mediaList.place(x=10,y=row2+25)

        row3= row2+200
        filterLabel=Label(self,text="Filter:")
        filterLabel.place(x=10,y=row3)
        if(platform.system() == 'Windows'):
            filterWidth = 15
        else:
            filterWidth = 8
        filterString.trace("w", lambda name, index, mode, filterString=filterString: updateFilter(filterString.get()))
        filterEntry = Entry(self, textvariable=filterString,width=filterWidth)
        filterEntry.place(x=45,y=row3)

        Label(self,text='ID Size:').place(x=130,y=row3)
        idSizeString.trace("w", lambda name, index, mode, idSizeString=idSizeString: updateIDSize(idSizeString.get()))
        idSizeEntry = Entry(self, textvariable=idSizeString, width=3)
        idSizeEntry.place(x=180,y=row3)
        
        Label(self,text='ID Mod:').place(x=225,y=row3)
        idMod.trace("w", lambda name, index, mode,  idMod=idMod: updateIDMod(idMod.get()))
        idModEntry = Entry(self, textvariable=idMod, width=5)
        idModEntry.place(x=280,y=row3)
        row4= row3+25
        Label(self, text='Media Per Filtered Server:').place(x=10,y=row4)
        fileDirectory.place(x=10, y= row4+25)

        row5= row4+200
        Label(self,text="Destination Folder:").place(x=10, y=row5)

        def updateConfig(lineItem,value):
            if '*' in value:
                configError.config(text=lineItem+' Can Not Use *')
            else:
                configError.config(text='')
                self.config = putterConfig.UpdateConfig(lineItem,value)
        if(platform.system() == 'Windows'):
            longWidths = 40
        else:
            longWidths = 30
        destinationFolder.trace("w", lambda name, index, mode, destinationFolder=destinationFolder: updateConfig('destinationFolder',destinationFolder.get()))
        destinationFolderEntry = Entry(self, width=longWidths, textvariable=destinationFolder)
        destinationFolderEntry.place(x=128,y=row5)

        row6 = row5+25
        Label(self,text="Destination Path:").place(x=10, y=row6)
  
        destinationPath.trace("w", lambda name, index, mode, destinationPath=destinationPath:updateConfig('destinationPath',destinationPath.get()))
        destinationPathEntry = Entry(self, width=longWidths, textvariable=destinationPath)
        destinationPathEntry.place(x=128,y=row6)

        row7 = row6+25
        Label(self,text="IP Schema:").place(x=10, y=row7)
      
        ipSchema.trace("w", lambda name, index, mode, ipSchema=ipSchema: updateConfig('ipSchema', ipSchema.get()))
        ipSchemaEntry = Entry(self, width=longWidths, textvariable=ipSchema)
        ipSchemaEntry.place(x=128,y=row7)
        
        Checkbutton(self,text='Overwrite Files',variable=overwriteFiles,onvalue=1,offvalue=0,command=setOverWrite).place(x=10,y=row7+25)

        Label(self,text='Concurrency:').place(x=200,y=row7+25)
        concurrency.trace("w", lambda name, index, mode,  concurrency=concurrency: updateConfig('concurrency',concurrency.get()))
        concurrencyEntry = Entry(self, textvariable=concurrency, width=5)
        concurrencyEntry.place(x=285,y=row7+25)
        row8 = row7+50
        
        configError.place(x=15,y=row8-20)
        Button(self, text="Start Transfer",command=startPutter).place(x=150,y=row8)


