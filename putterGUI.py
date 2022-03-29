import tkinter as tk
from tkinter import tix
from putterConfigPage import ConfigPage
from putterMainPage import MainPage
from putterTransferPage import TransferPage


class Page(tix.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        
        def changePage(page):
            print(page)
            if page =='Main':
                p1.show()
                return p1
      

        p1 = MainPage(self)
        p2 = ConfigPage(self)
       # p3 = TransferPage(self)
    
        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
      #  p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Page 1", command=p1.show)
        b2 = tk.Button(buttonframe, text="Preferences", command=p2.show)
       # b3 = tk.Button(buttonframe, text="Start Transfer", command=p3.show)

        p1.show()

if __name__ == "__main__":
    root = tix.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.title("mediaPutter")
    root.geometry("400x600+120+120")
    root.mainloop()