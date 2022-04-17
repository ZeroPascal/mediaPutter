import tkinter as tk
#from tkinter import tix
from putterMainPage import MainPage
from putterTransferPage import TransferPage


class Page(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
    def show(self):
        self.lift()


class MainView(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container= tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
     
        self.title("mediaPutter v2.4.4")
        self.geometry("425x687+120+120")
        self.frames = {}
        for F in (MainPage,TransferPage):
            frame = F(container,self)
            self.frames[frame.name]=frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.frames['MainPage'].tkraise()
  
    # to display the current frame passed as
    # parameter

    def quitTransfer(self):
        self.frames['MainPage'].tkraise()

    def startTransfer(self, serverList,config):
       
        transfer = self.frames['TransferPage']
        transfer.start(serverList,config)
        transfer.tkraise()
  

      

       # p1 = MainPage(changePage)
        #p2 = TransferPage()
       # p3 = TransferPage(self)
    
        #buttonframe = tk.Frame(self)
        #container = tk.Frame(self)
        #buttonframe.pack(side="top", fill="x", expand=False)
        #container.pack(side="top", fill="both", expand=True)

        #p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        #p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
      #  p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        #b1 = tk.Button(buttonframe, text="Page 1", command=p1.show)
       
        #b2 = tk.Button(buttonframe, text="Preferences", command=p2.show)
        
       # b3 = tk.Button(buttonframe, text="Start Transfer", command=p3.show)


        #p1.show()

if __name__ == "__main__":
    root = MainView()
    root.mainloop()