__author__ = 'jack'
import numpy as np
from atom.api import Typed, List, Float, Bool
from OpenGL.GL import *
from enaml_opengl.scenegraph_node import GraphicsNode, d_
from enaml_opengl.geometry import Vec3d

class AxisItem(GraphicsNode):
    """ An Axis Item

    Shows a coordinate origin.

    x=blue
    y=yellow
    z=green
    """

    antialias  = d_(Bool(True))
    size       = d_(Typed(Vec3d, factory=lambda: Vec3d(1.0, 1.0, 1.0)))
    line_width = d_(Float(1.0))
    colors     = d_(List())

    def _default_colors(self):
        return [(1, 0, 0, 0.6),  # x red
               (0, 1, 0, 0.6),  # y green
               (0, 0, 1, 0.6),  # z blue
               ]

    def render_node(self, context):
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        #glEnable( GL_BLEND )
        #glEnable( GL_ALPHA_TEST )

        super(AxisItem, self).render_node(context)

        glPushAttrib(GL_LINE_BIT)

        glLineWidth(self.line_width)

        colors = self.colors

        if self.antialias:
            glEnable(GL_LINE_SMOOTH)
            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

        glBegin(GL_LINES)
        v = self.size

        glColor4f(*colors[2])  # z is green
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, v.z)

        glColor4f(*colors[1])  # y is yellow
        glVertex3f(0, 0, 0)
        glVertex3f(0, v.y, 0)

        glColor4f(*colors[0])  # x is blue
        glVertex3f(0, 0, 0)
        glVertex3f(v.x, 0, 0)

        glEnd()

        glPopAttrib()

