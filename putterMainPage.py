
from tkinter import *
from tkinter import tix
from tkinter import filedialog
from os import listdir
from os.path import isfile, join
import putterBrains
import putterConfig
import re

class Page(tix.Frame):
    def __init__(self, *args, **kwargs):
        tix.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class MainPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
       
        self.filePath = ''
        self.mediaFiles = []
        self.selectedMediaFiles = []
        self.serverList = {}

        def selectMediaFolder():
            global mediaFiles
            
            try:
                filePath = filedialog.askdirectory()
            except:
                filePath = ''
            if filePath:
                mediaList.delete(0,mediaList.size())
                mediaFiles = [f for f in listdir(filePath) if isfile(join(filePath, f))]
                i=0
                
                for file in mediaFiles:
                    i+=1
                    mediaList.insert(i,file)
                
                mediaList.update()
                updateFilter(filterString)

        def updateSelectedMedia(evt):
            global mediaList
            #global selectedMediaFiles

            s = mediaList.curselection()
            self.selectedMediaFiles= []
            for i in s:
                self.selectedMediaFiles.append(mediaList.get(i))
            #print('Selected Media Files:' ,selectedMediaFiles)
            updateFilter(filterString)

        def startPutter():
            putterBrains.Putt(self.serverList,destinationString.get())
            
        def updateDestination(dest):
            putterConfig.UpdateConfig('destinationFolder',dest.get())

        def updateFilter(filter):
           
            putterConfig.UpdateConfig('filter',filter.get())
            filterExample.config(text="*"+filter.get()+"*")
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

        Button(self, text="Select Media Folder",command=selectMediaFolder).place(x=10,y=10)

        Label(self,text='Media Files (Select to ignore):').place(x=10,y=40)
        mediaList = Listbox(self, width=55, selectmode=EXTENDED, name='mediaList')
        mediaList.bind('<<ListboxSelect>>', updateSelectedMedia)
        #mediaList.xview()
        #mediaList.yview()
        mediaList.place(x=10,y=65)

        row2= 250
        filterLabel=Label(self,text="Filter:")
        filterLabel.place(x=10,y=row2)
        filterString =StringVar()
        filterString.set(putterConfig.getConfig('filter'))
        filterString.trace("w", lambda name, index, mode, filterString=filterString: updateFilter(filterString))
        filterEntry = Entry(self, textvariable=filterString)
        filterEntry.place(x=45,y=row2)

        filterStringExample =''
        filterExample=Label(self,text=filterStringExample)
        filterExample.place(x=175,y=row2)
        Label(self, text='Media Per Filtered Server:').place(x=10,y=row2+30)
        fileDirectory = tix.HList(self,width=55)
        fileDirectory.place(x=10, y= row2+55)

        row4= 450
        Label(self,text="Destination Folder:").place(x=10, y=row4)

        destinationString =StringVar()
        destinationString.trace("w", lambda name, index, mode, destinationString=destinationString: updateDestination(destinationString))
        destinationEntry = Entry(self, textvariable=destinationString)
        destinationEntry.place(x=120,y=row4)

        Button(self, text="Putt!",command=startPutter).place(x=150,y=row4+50)

        def startConfig():
            putterConfig.ReadConfig()

        Button(self, text="Config",command=startConfig).place(x=150,y=row4+90)


