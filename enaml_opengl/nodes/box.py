__author__ = 'jack'
import numpy as np
from atom.api import Typed, Value, observe
from OpenGL.GL import *
from enaml_opengl.scenegraph_node import GraphicsNode, d_
from enaml_opengl.geometry import Vec3d

class BoxItem(GraphicsNode):
    """ An Box Item

    """

    size = d_(Typed(Vec3d, factory=lambda: Vec3d(1.0, 1.0, 1.0)))
    color = d_(Value([1.0, 1.0, 1.0, 0.5]))

    @observe("size", "color")
    def _bi_trigger_update(self, change):
        self.trigger_update()



    def render_node(self, context):
        super(BoxItem, self).render_node(context)

        glBegin( GL_LINES )

        glColor4f(*self.color)
        x,y,z = self.size

        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, z)

        glVertex3f(x, 0, 0)
        glVertex3f(x, 0, z)

        glVertex3f(0, y, 0)
        glVertex3f(0, y, z)

        glVertex3f(x, y, 0)
        glVertex3f(x, y, z)

        glVertex3f(0, 0, 0)
        glVertex3f(0, y, 0)

        glVertex3f(x, 0, 0)
        glVertex3f(x, y, 0)

        glVertex3f(0, 0, z)
        glVertex3f(0, y, z)

        glVertex3f(x, 0, z)
        glVertex3f(x, y, z)

        glVertex3f(0, 0, 0)
        glVertex3f(x, 0, 0)

        glVertex3f(0, y, 0)
        glVertex3f(x, y, 0)

        glVertex3f(0, 0, z)
        glVertex3f(x, 0, z)

        glVertex3f(0, y, z)
        glVertex3f(x, y, z)

        glEnd()
