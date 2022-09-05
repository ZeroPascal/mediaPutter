import platform
from tkinter import *
from turtle import pu
from nasScanner import nasScanner
import putterConfig

class NASPopup(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.name='NASPopup'
        self.controller= controller
        self.config = putterConfig.ReadConfig()
        nasPathString =StringVar()
        nasPathString.set(self.config.get('nasPath'))
        nasUserString= StringVar()
        nasUserString.set(self.config.get('nasUser'))
        nasFolderString= StringVar()
        nasFolderString.set(self.config.get('nasFolder'))

        if(platform.system() == 'Windows'):
             listWidth = 65
        else:
            listWidth = 50   
        mediaList = Listbox(self, width=listWidth, selectmode=EXTENDED, name='mediaList')
        

        def updateNASPath(nasPath:str):
            putterConfig.UpdateConfig('nasPath',nasPath)
        
        def updateNASFolder(nasFolder:str):
            putterConfig.UpdateConfig('nasFolder',nasFolder)
        
        def updateNASUser(nasUser:str):
            putterConfig.UpdateConfig('nasUser',nasUser)

        def scanPath():
            mediaList.delete(0,mediaList.size())
            files= nasScanner(putterConfig.getConfig('nasUser'),putterConfig.getConfig('nasPath'),putterConfig.getConfig('nasFolder'))
            i = 0
            for file in files:
                i+=1
                mediaList.insert(i,file)
                

        def updateSelectedMedia():
            print()
        
        def acceptFiles():
            putterConfig.UpdateConfig('useNAS',1)
            self.controller.quitNAS()
        
        def cancelNAS():
            putterConfig.UpdateConfig('useNAS',0)
            self.controller.quitNAS()

        row1= 10
       # Button(self, text="Select Media ").place(x=10,y=10)

        row2= row1+25
        Label(self,text='Enter NAS (user@serverIP):').place(x=10,y=row2)

        row3= row2+25
        nasUserString.trace("w", lambda name, index, mode, nasUserString=nasUserString: updateNASUser(nasUserString.get()))
        nasUser = Entry(self, textvariable=nasUserString,width=55)
        nasUser.place(x=25,y=row3)

        row4= row3+25
        Label(self,text='Enter NAS Path (/path/to/user/directory/):').place(x=10,y=row4)

        row5= row4+25
        nasPathString.trace("w", lambda name, index, mode, nasPathString=nasPathString: updateNASPath(nasPathString.get()))
        nasPath = Entry(self, textvariable=nasPathString,width=55)
        nasPath.place(x=25,y=row5)

        row6 = row5+25
        Label(self,text='Folder Path (path/from/user/directory):').place(x=10,y=row6)
        
        row7 =row6+25
        nasFolderString.trace("w", lambda name, index, mode, nasFolderString=nasFolderString: updateNASFolder(nasFolderString.get()))
        nasFolder = Entry(self, textvariable=nasFolderString,width=55)
        nasFolder.place(x=25,y=row7)

        row8=row7+25
        Button(self, text="Scan Path",command=scanPath).place(x=10,y=row8)

        row9= row8+35
        Label(self,text='Items found in path:').place(x=10,y=row9)
        mediaList.bind('<<ListboxSelect>>', updateSelectedMedia)
        mediaList.place(x=10,y=row9+25)

        row10=row9+200
        Button(self, text="Accept Files",command=acceptFiles).place(x=25,y=row10)
        Button(self, text="Cancel",command=cancelNAS).place(x=150,y=row10)

