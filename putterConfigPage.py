from tkinter import *
from tkinter import tix

from putterConfig import ReadConfig, UpdateConfig

class Page(tix.Frame):
    def __init__(self, *args, **kwargs):
        tix.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

def update(item, value):
    UpdateConfig(item,value)

class ConfigPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        config = ReadConfig()
        row=10
        i=0
        values=[]
        for item , att in config.items():
            Label(self,text=item).place(x=10,y=row)
            values.append(StringVar())
            currentValue = values[i]
            currentValue.set(att)
            currentValue.trace("w", lambda name, index, mode, currentValue=currentValue: update(item,currentValue.get()))
            Entry(self,textvariable=currentValue, width=30).place(x=125, y=row)
            row+=20
            i+=1
