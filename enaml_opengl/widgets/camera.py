__author__ = 'jack'
import numpy as np

from atom.api import Atom, Typed, Float, observe
from OpenGL.GL import (glMatrixMode, glLoadIdentity, glMultMatrixf,
                       GL_PROJECTION, GL_MODELVIEW)

from .viewport import Viewport, PerspectiveViewport


class Camera(Atom):

    #: the camera viewport
    viewport = Typed(Viewport)

    #: the projection matrix
    projection_matrix = Typed(np.ndarray)

    #: the modelview matrix
    modelview_matrix  = Typed(np.ndarray)

    #: initialize default viewport
    def _default_viewport(self):
        return PerspectiveViewport()

    #: initialize default projection matrix
    def _default_projection_matrix(self):
        # XXX invalid projection matrix !!!
        return np.eye(4)

    #: initialize default modelview matrix
    def _default_modelview_matrix(self):
        return np.eye(4)

    def render(self):
        """
        render projection and modelview matrix
        :return: None
        """
        self.viewport.render()

        # setup projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMultMatrixf(self.projection_matrix.transpose())

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glMultMatrixf(self.modelview_matrix.transpose())



class PinholeCamera(Camera):

    near = Float(0.001)
    far  = Float(1000.)
    fov  = Float(60)


    @observe("viewport.x", "viewport.y", "viewport.width", "viewport.height",
             "near", "far", "fov")
    def _update_projection_matrix(self, change):
        """
        :param change:

        recomputes the projection matrix if any of the inputs chnage
        :return:
        """
        vp = self.viewport

        r = self.near * np.tan(self.fov * 0.5 * np.pi / 180.)
        t = r * vp.height / vp.width

        left = r * (vp.x * (2. / vp.width) - 1)
        right = r * (vp.width * (2. / vp.width) - 1)
        bottom = t * (vp.y * (2. / vp.height) - 1)
        top = t * (vp.height * (2. / vp.height) - 1)

        self.projection_matrix = self.viewport.calculate_projection_matrix(left, right, bottom, top,
                                                                           self.near, self.far, self.fov)