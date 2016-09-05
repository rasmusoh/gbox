from Tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

tmap = np.zeros(1000,1000)

terrains = ("PLAINS", "SEA", "FRESHWATER", "MOUNTAIN", "ROAD")
modes = ("DRAW", "CALC")
 
class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack() 

        self.button = Button(
                frame, text="QUIT", fg="red", command=frame.quit
                )
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=LEFT)

        self.terrain = StringVar()
        self.terrain.set("PLAINS")

        self.mode = StringVar()
        self.mode.set("DRAW")

        self.terrainsMenu = SelectorMenu(master, terrains, self.terrain)
        self.modesMenu = SelectorMenu(master, modes, self.mode)

        fig = plt.figure(1)

        mapviz = tmap

        plt.imshow(grid)
        plt.axis('off')

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.show()
        canvas.get_tk_widget().pack()

    def say_hi(self):
        print self.terrain.get()

class SelectorMenu:

    def __init__(self, master, options, var):

        frame = Frame(master)
        frame.pack() 

        for option in options:
            Radiobutton(frame, text= option, variable=var, value=option).pack(anchor=W)

root = Tk()

app = App(root)

root.mainloop()
root.destroy()


