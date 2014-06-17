from __future__ import division

import numpy as np
from atom.api import Atom, Int
from OpenGL.GL import glViewport

class Viewport(Atom):

    x = Int(0)
    y = Int(0)

    width = Int(800)
    height = Int(600)

    def render(self):
        glViewport(self.x, self.y, self.width, self.height)

    def calculate_projection_matrix(self, left, right, bottom, top, near, far, fov=None):
        raise NotImplementedError

class OrthoViewport(Viewport):

    def calculate_projection_matrix(self, left, right, bottom, top, near, far, fov=None):
        tx = -1.*float(right + left)/float(right - left)
        ty = -1.*float(top + bottom)/float(top - bottom)
        tz = -1.*float(far + near)/float(far - near)
        return np.array([2./float(right-left), 0, 0, tx,
                         0, 2./float(top-bottom), 0, ty,
                         0, 0, -2./float(far-near), tz,
                         0, 0, 0, 1.], dtype=np.float64).reshape(4,4)

class PerspectiveViewport(Viewport):

    def calculate_projection_matrix(self, left, right, bottom, top, near, far, fov):
        f = 1./np.tanh(fov/2.)
        aspect = float(right - left) / float(bottom - top)
        return np.array([f/aspect, 0, 0, 0,
                         0, f, 0, 0,
                         0, 0, float(far+near)/float(near-far), float(2*far*near)/float(near-far),
                         0, 0, -1, 0], dtype=np.float64).reshape(4,4)
