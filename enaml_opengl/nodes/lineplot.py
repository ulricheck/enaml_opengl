__author__ = 'jack'
import numpy as np
from atom.api import Value, Coerced
from OpenGL.GL import *
from enaml_opengl.scenegraph_node import GraphicsNode, d_

class LinePlotItem(GraphicsNode):
    """ An LinePlot Item

    """

    #: (N,3) array of floats specifying line point locations.
    pos = d_(Coerced(np.ndarray, coercer=np.ndarray))

    #: (N,4) array of floats (0.0-1.0) specifying pot colors
    #: OR a tuple of floats specifying a single color for all spots.
    color = d_(Value([1.0, 1.0, 1.0, 0.5]))

    linewidth = d_(Value(1.0))

    def render_node(self, context):
        super(LinePlotItem, self).render_node(context)
        glPushAttrib(GL_LINE_BIT)

        glEnableClientState(GL_VERTEX_ARRAY)
        try:
            glVertexPointerf(self.pos)

            if isinstance(self.color, np.ndarray):
                glEnableClientState(GL_COLOR_ARRAY)
                glColorPointerf(self.color)
            else:
                glColor4f(*self.color)
            glLineWidth(self.linewidth)
            #glPointSize(self.width)

            if self.antialias:
                glEnable(GL_LINE_SMOOTH)
                glEnable(GL_BLEND)
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
                glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);

            glDrawArrays(GL_LINE_STRIP, 0, int(self.pos.size / self.pos.shape[-1]))
        finally:
            glDisableClientState(GL_COLOR_ARRAY)
            glDisableClientState(GL_VERTEX_ARRAY)

        glPopAttrib()
