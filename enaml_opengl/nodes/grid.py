__author__ = 'jack'
import numpy as np
from atom.api import Typed, List, Float, Bool
from OpenGL.GL import *
from enaml_opengl.scenegraph_node import GraphicsNode, d_
from enaml_opengl.geometry import Vec3d

class GridItem(GraphicsNode):
    """ An Grid Item

    """

    size = d_(Typed(Vec3d, factory=lambda: Vec3d(1.0, 1.0, 1.0)))

    def render_node(self, context):
        super(GridItem, self).render_node(context)

        if self.antialias:
            glEnable(GL_LINE_SMOOTH)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

        glBegin( GL_LINES )

        # size is not used here ..
        glColor4f(1, 1, 1, .3)
        for x in range(-10, 11):
            glVertex3f(x, -10, 0)
            glVertex3f(x,  10, 0)
        for y in range(-10, 11):
            glVertex3f(-10, y, 0)
            glVertex3f( 10, y, 0)

        glEnd()