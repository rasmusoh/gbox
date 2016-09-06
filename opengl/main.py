from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
    
class Tree:
    def __init__(self, root, length, angle, gens):
        self.root = root
        self.tip = [root[0] + length*math.cos(angle),root[1] + length*math.sin(angle)]
        self.children = []
        degen = 0.8
        if gens > 1:
            self.children = [Tree(self.tip, length*degen, angle-math.pi/4, gens-1),
                             Tree(self.tip, length*degen, angle+math.pi/4, gens-1)]
            
    def get_lines(self):
        lines = [self.root, self.tip]
        for child in self.children:
            lines.extend(child.get_lines())
        return lines

treelines = Tree([500.0,0.0], 100, math.pi/2,  10).get_lines()
window = 0                                             # glut window number
width, height = 1000, 1000                               # window size

def draw():                                            # ondraw is called all the time
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear the screen 
    glLoadIdentity()                                   # reset position
    refresh2d(width, height)

    glColor3f(0.0, 0.0, 1.0)                           # set color to blue
    draw_lines(treelines)

    glutSwapBuffers()                                  # important for double buffering

def draw_rect(x, y, width, height):
    glBegin(GL_QUADS)                                  # start drawing a rectangle
    glVertex2f(x, y)                                   # bottom left point
    glVertex2f(x + width, y)                           # bottom right point
    glVertex2f(x + width, y + height)                  # top right point
    glVertex2f(x, y + height)                          # top left point
    glEnd()                                            # done drawing a rectangle

def draw_line(start, end):
    glBegin(GL_LINES)                                  # start drawing a line
    glVertex2f(start[0], start[1])                     # bottom left point
    glVertex2f(end[0], end[1])                         # bottom right point
    glEnd()                                            # done drawing a rectangle

def draw_lines(points):
    glBegin(GL_LINES)                                  # start drawing a line
    for point in points:
        glVertex2f(point[0], point[1])                     # bottom left point
    glEnd()                                            # done drawing a rectangle

def draw_curve(points):
    glBegin(GL_LINES)                                  
    for i in range(0,len(points)-1):
        glVertex2f(points[i][0], points[i][1])
        glVertex2f(points[i+1][0], points[i+1][1])
    glEnd()

def draw_tree(start, startlen, gens):
    draw_lines()

def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()
            


def main():
    # initialization
    glutInit()                                             # initialize glut
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(width, height)                      # set window size
    glutInitWindowPosition(0, 0)                           # set window position
    window = glutCreateWindow("Grow.")              # create window with title
    glutDisplayFunc(draw)                                  # set draw function callback
    glutIdleFunc(draw)                                     # draw all the time
    glutMainLoop()                                         # start everything

import cProfile as profile
profile.run('main()')
