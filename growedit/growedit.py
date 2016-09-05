import Tkinter as tk
import math
import radialtree
import hyphal

shortcuts_inc = ('q','w','e','r','t','y','u','i')
shortcuts_dec = ('a','s','d','f','g','h','j','k')
class GrowEdit(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.icons = { 
            "MOVE" : tk.PhotoImage(file = "../icons/move-small.gif"),
            "ADD" :tk.PhotoImage(file = "../icons/add-small.gif"),
            "CONNECT":tk.PhotoImage(file = "../icons/connect-small.gif"),
            "ERASE":tk.PhotoImage(file = "../icons/erase-small.gif"),
            "BA":tk.PhotoImage(file = "../icons/ba-small.gif"),
            "TREE":tk.PhotoImage(file = "../icons/tree-small.gif"),
            "NEIGHBOUR":tk.PhotoImage(file = "../icons/neighbour-small.gif"),
            "PLAY":tk.PhotoImage(file = "../icons/play-small.gif"),
            "PAUSE": tk.PhotoImage(file = "../icons/pause-small.gif")}

        ## maximize window
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))

        # create a canvas
        self._canvas = tk.Canvas(width=400, height=400)
        self._canvas.pack(fill="both", expand=True, side = tk.LEFT)
        self._canvas.create_rectangle(0, 0, 5000, 5000, fill='white', tags='bg')
        
        self.sidebar = tk.Frame(self)
        self.sidebar.pack(side=tk.RIGHT)
        self.playbutton = tk.Button(self.sidebar, command = self.playpause) 
        self.playbutton.pack()
        self.configframe = tk.Frame(self.sidebar)
        self.configframe.pack()


        self.bind("<Key>", self.key_press)
        self._canvas.bind("<ButtonPress-1>", self.mouse_click)

        self.growthmodes = {
                    "RADIAL": radialtree.RadialTreeMode(self.configframe, self._canvas),
                    "HYPHAL": hyphal.HyphalMode(self.configframe, self._canvas),
                    "PUSHHYPHAL": hyphal.PushHyphalMode(self.configframe, self._canvas)
                }
        self.growthmode = tk.StringVar()
        self.growthmode.trace('w', self.modechanged)
        self.growthmode.set(self.growthmodes.keys()[0])
        self.mode_menu = apply(tk.OptionMenu, (self.sidebar, self.growthmode) + tuple(self.growthmodes.keys()))
        self.mode_menu.pack()

        self.running = False

    def current_mode(self):
        return self.growthmodes[self.growthmode.get()]

    def modechanged(self, *args):
        self.current_mode().select()

    def stop(self):
        self.running = false
        self.playbutton.config( image = self.icons["PLAY"])

    def run(self):
        self.running = True
        self.playbutton.config( image = self.icons["PAUSE"])
        self.update()

    def playbutton_click(self, event):
        self.playpause()

    def mouse_click(self, event):
        self.current_mode().set_start((event.x, event.y))

    def playpause(self):
        if running:
            self.stop()
        else:
            self.run()

    def update(self):
        if self.running:
            self._canvas.after(branchrate, self.update)
    

    def key_press(self, event):
        if event.char == ' ': 
            self.playpause()
        elif event.char == 'c': 
            self.clear()
        elif event.char in shortcuts_inc:
            self.current_mode().increase_param(shortcuts_inc.index(event.char))
        elif event.char in shortcuts_dec:
            self.current_mode().decrease_param(shortcuts_dec.index(event.char))
        pass

    def clear(self):
        self._canvas.delete("branch")

if __name__ == "__main__":
    app = GrowEdit()
    app.update()
    app.mainloop()


