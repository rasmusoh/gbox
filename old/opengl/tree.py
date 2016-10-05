import numpy as np

class Tree:
    def __init__(self, root, length, angle, gens):
        self.root = root
        self.tip = root + length*np.array([np.cos(angle), np.sin(angle)], dtype=np.float32)
        self.children = []
        degen = 0.8
        if gens > 1:
            self.children = [Tree(self.tip, length*degen, angle-np.pi/4, gens-1),
                             Tree(self.tip, length*degen, angle+np.pi/4, gens-1)]
            
    def get_lines(self):
        lines = [self.root, self.tip]
        for child in self.children:
            lines.extend(child.get_lines())
        return lines

    def get_lines_np(self):
        return np.array(self.get_lines())

