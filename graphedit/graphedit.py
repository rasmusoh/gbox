import igraph as ig
import Tkinter as tk
from modes import *
from rules import *
import math

mode_descriptions = {
             "MOVE":"Move verteces(Q)",
             "ADD":"Add/Resize vertex(A)",
             "CONNECT": "Connect vertex(C)",
             "TREE": "Grow a vertex network tree-like(T)",
             "BA": "Add nodes according to Barabasi-Albert algorithm(B)",
             "NEIGHBOUR": "Add edges using nearest neighbour(N)",
             "ERASE":"Erase(E)"}
mode_modifier_variables = {
             "ADD": "Initial connections",
             "TREE": "Child nodes at each level",
             "BA": "Initial connections"}
mode_shortcuts = {"q" : "MOVE",
                 "w" : "ADD",
                 "e" : "CONNECT",
                 "r" : "ERASE"}

class GraphEdit(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        ## maximize window
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))
        
	self._graph = ig.Graph()

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

        # create a canvas
        self._canvas = tk.Canvas(width=400, height=400)
        self._canvas.pack(fill="both", expand=True, side = tk.LEFT)
        self._canvas.create_rectangle(0, 0, 5000, 5000, fill='white', tags='bg')

        self.sidebar = tk.Frame(self)
        self.sidebar.pack(side=tk.RIGHT)

        self.modvar = tk.IntVar()
        self.modvar.set(1)
        self.modvarentry = tk.Spinbox(self.sidebar, from_=0, to=10, textvariable = self.modvar)
        self.modvarentry.pack()


        self.modes = {
                "MOVE": MoveMode(self._canvas, self._graph, self.modvar),
                "ADD": AddMode(self._canvas, self._graph, self.modvar), 
                "CONNECT": ConnectMode(self._canvas, self._graph, self.modvar),
                "ERASE": EraseMode(self._canvas, self._graph, self.modvar),
                "BA": BarabasiMode(self._canvas, self._graph, self.modvar),
                "TREE": TreeMode(self._canvas, self._graph, self.modvar),
                "NEIGHBOUR": NeighbourMode(self._canvas, self._graph, self.modvar)
                }
        self.mode = tk.StringVar()
        self.mode.set(self.modes.keys()[0])
        self.mode_menu = SelectorMenu(self.sidebar, self.modes.keys(), mode_descriptions, self.mode, self.icons)

        self.rules = allrules
        self.current_rule = tk.StringVar()
        self.current_rule.set(self.rules.keys()[1])
        self.rule_menu = tk.OptionMenu(self.sidebar, self.current_rule, *self.rules.keys(), command = self.changerule) 
        self.rule_menu.pack()

        self.bind("<Key>", self.key_press)
        self._canvas.bind("<ButtonRelease-1>", self.mouse_release)
        self._canvas.bind("<B1-Motion>", self.mouse_move)
        self._canvas.tag_bind("vertex", "<ButtonPress-1>", self.vertex_click)
        self._canvas.tag_bind("bg", "<ButtonPress-1>", self.bg_click)

        self.running = False

    def changerule(self, val):
        self.rules[self.current_rule.get()].changeto(self._graph)

    def mouse_release(self, event):
        if not self.running:
            self.modes[self.mode.get()].mouse_release(event)
            self._render_graph()

    def bg_click(self, event):
        if not self.running:
            self.modes[self.mode.get()].bg_click(event)
            self._render_graph()

    def vertex_click(self, event):
        if not self.running:
            self.modes[self.mode.get()].vertex_click(event)
            self._render_graph()

    def mouse_move(self, event):
        if not self.running:
            self.modes[self.mode.get()].mouse_move(event)
            self._render_graph()

    def key_press(self, event):
        if event.char in mode_shortcuts.keys(): 
            self.mode.set(mode_shortcuts[event.char])
        elif event.char == ' ':
            if self.running:
                self.stop()
            else:
                self.run()

    def run(self):
        self.rules[self.current_rule.get()].simulate_start(self._graph, self._canvas.winfo_width(), self._canvas.winfo_height())
        self.running = True

    def stop(self):
        self.running = False

    def update(self):
        if self.running:
            self.rules[self.current_rule.get()].simulate_step(self._graph)
            self._render_graph()
        self._canvas.after(1, self.update)

    def _render_graph(self):
        self._canvas.delete("vertex")
        self._canvas.delete("edge")
        for v in self._graph.vs:
            self._draw_vertex(v)
        for e in self._graph.get_edgelist():
            self._draw_edge(e)

    def _draw_vertex(self, v):
        (x,y) = v["coord"]
        size = v["size"]
        color = "black"
        dispSize = math.sqrt(size)
        self._canvas.create_oval(x-dispSize, y-dispSize, x+dispSize, y+dispSize, 
            outline=color, fill=color, tags=("vertex", str(v.index)) )

    def _draw_edge(self, e):
        fromX, fromY = self._graph.vs[e[0]]["coord"]
        toX, toY = self._graph.vs[e[1]]["coord"]
        self._canvas.create_line(fromX, fromY, toX, toY, tags=("edge"))


class SelectorMenu:

    def __init__(self, master, options, names, var, icons):

        frame = tk.Frame(master)
        frame.pack() 

        col = 0
        for option in options:
            button = tk.Radiobutton(frame, text = names[option], variable=var, value=option, image = icons[option],
                    indicatoron = 0).grid(column = col)
            col = (col + 1) % 2


if __name__ == "__main__":
    app = GraphEdit()
    app.update()
    app.mainloop()
