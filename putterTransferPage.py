from tkinter import *
from tkinter import tix

class Page(tix.Frame):
    def __init__(self, *args, **kwargs):
        tix.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class TransferPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)