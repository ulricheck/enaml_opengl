__author__ = 'jack'
import numpy as np
from atom.api import Typed, List, Float, Bool
from OpenGL.GL import *
from enaml_opengl.scenegraph_node import GraphicsNode
from enaml_opengl.geometry import Vec3d

class AxisItem(GraphicsNode):
    """ An Axis Item

    Shows a coordinate origin.

    x=blue
    y=yellow
    z=green
    """

    antialias  = Bool(True)
    size       = Typed(Vec3d, factory=lambda: Vec3d(1.0, 1.0, 1.0))
    line_width = Float(1.0)
    colors     = List([(1, 0, 0, 0.6),  # x red
                       (0, 1, 0, 0.6),  # y green
                       (0, 0, 1, 0.6),  # z blue
                       ])


    def render_node(self, context):
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        #glEnable( GL_BLEND )
        #glEnable( GL_ALPHA_TEST )

        super(AxisItem, self).render_node(context)

        if self.antialias:
            glEnable(GL_LINE_SMOOTH)
            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

        glBegin( GL_LINES )

        v = self.size
        glColor4f(0, 1, 0, .6)  # z is green
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, v.z)

        glColor4f(1, 1, 0, .6)  # y is yellow
        glVertex3f(0, 0, 0)
        glVertex3f(0, v.y, 0)

        glColor4f(0, 0, 1, .6)  # x is blue
        glVertex3f(0, 0, 0)
        glVertex3f(v.x, 0, 0)
        glEnd()
        