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
    modelview_matrix  = Typed(np.ndarray, factory=lambda: np.identity(4))

    #: initialize default viewport
    def _default_viewport(self):
        return PerspectiveViewport()

    #: initialize default projection matrix as pinhole camera
    def _default_projection_matrix(self):
        vp = self.viewport
        left, right, bottom, top = self._device_coordinates()
        return vp.calculate_projection_matrix(left, right, bottom, top,
                                              0.001, 1000., 60)

    def setup(self):
        """
        render projection and modelview matrix
        :return: None
        """
        self.viewport.setup()

        # setup projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMultMatrixf(self.projection_matrix.transpose())

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glMultMatrixf(self.modelview_matrix.transpose())


    def _device_coordinates(self):
        vp = self.viewport.box

        r = self.near * np.tan(self.fov * 0.5 * np.pi / 180.)
        t = r * vp.height / vp.width

        left = r * (vp.x * (2. / vp.width) - 1)
        right = r * (vp.width * (2. / vp.width) - 1)
        bottom = t * (vp.y * (2. / vp.height) - 1)
        top = t * (vp.height * (2. / vp.height) - 1)
        return (left, right, bottom, top)


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
        left, right, bottom, top = self._device_coordinates()
        self.projection_matrix = self.viewport.calculate_projection_matrix(left, right, bottom, top,
                                                                           self.near, self.far, self.fov)