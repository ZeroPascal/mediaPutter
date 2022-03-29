import tkinter as tk
from tkinter import tix

class TransferPage():
    def __init__(self, master, cancel, hide):
        
        self.window = tk.Toplevel(master)
        self.window.title("mediaPutter")
        self.window.geometry("400x600+120+120")
        tk.Label(self.window,text='Transfer Log').place(x=10, y=10)
        self.log=tix.HList(self.window,width=55,height=15)
        self.log.place(x=10,y=30)
        self.cancelCallback = cancel
        self.hideCallback = hide
        self.logFeedback = ()
        def cancelTransfer():
           
            self.cancelCallback()
            

        self.cancelButton = tk.Button(self.window,text='Cancel',command=self.window.destroy)
        self.cancelButton.place(x=10,y=250)

      

    
     

        
       