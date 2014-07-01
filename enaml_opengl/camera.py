__author__ = 'jack'
import numpy as np

from atom.api import Atom, Typed, Float, observe
from enaml.core.api import Declarative
from enaml.core.declarative import d_

from OpenGL.GL import (glMatrixMode, glLoadIdentity, glMultMatrixf,
                       GL_PROJECTION, GL_MODELVIEW)

from .viewport import Viewport, PerspectiveViewport


class Camera(Declarative):

    #: the camera viewport
    viewport = d_(Typed(Viewport))

    #: the projection matrix
    projection_matrix = d_(Typed(np.ndarray))

    #: the modelview matrix
    modelview_matrix  = d_(Typed(np.ndarray, factory=lambda: np.identity(4)))
    inv_modelview_matrix  = d_(Typed(np.ndarray, factory=lambda: np.identity(4)))

    near = d_(Float(0.001))
    far  = d_(Float(10.))

    #: initialize default viewport
    def _default_viewport(self):
        return PerspectiveViewport()

    #: initialize default projection matrix as pinhole camera
    def _default_projection_matrix(self):
        vp = self.viewport
        # initialize with some default FOV in case the subclass does not specifiy it.
        fov = 60
        if hasattr(self, "fov"):
            fov = self.fov
        left, right, bottom, top = self._device_coordinates(vp, fov)
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
        glMultMatrixf(self.projection_matrix.T)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glMultMatrixf(self.inv_modelview_matrix.T)

    def _device_coordinates(self, vp, fov):
        box = vp.box
        r = self.near * np.tan(fov * 0.5 * np.pi / 180.)
        t = r * box.height / box.width

        left = r * (box.x * (2. / box.width) - 1)
        right = r * (box.width * (2. / box.width) - 1)
        bottom = t * (box.y * (2. / box.height) - 1)
        top = t * (box.height * (2. / box.height) - 1)
        return (left, right, bottom, top)

    @observe("modelview_matrix")
    def _update_inv_mv(self, change):
        self.inv_modelview_matrix = np.linalg.inv(self.modelview_matrix)


class PinholeCamera(Camera):

    fov  = d_(Float(60))


    @observe("viewport.box", "near", "far", "fov")
    def _update_projection_matrix(self, change):
        """
        :param change:

        recomputes the projection matrix if any of the inputs chnage
        :return:
        """
        left, right, bottom, top = self._device_coordinates(self.viewport, self.fov)
        self.projection_matrix = self.viewport.calculate_projection_matrix(left, right, bottom, top,
                                                                           self.near, self.far, self.fov)

