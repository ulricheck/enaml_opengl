from __future__ import division

import numpy as np
from atom.api import Atom, Int, Value
from enaml.core.api import Declarative
from enaml.core.declarative import d_

from OpenGL.GL import glViewport

from .geometry import Rect

class Viewport(Declarative):

    box = Value(Rect, factory=lambda:Rect(x=0, y=0, width=800, height=600))

    def setup(self):
        box = self.box
        glViewport(box.x, box.y, box.width, box.height)

    def calculate_projection_matrix(self, left, right, bottom, top, near, far, fov=None):
        raise NotImplementedError

class OrthoViewport(Viewport):

    def calculate_projection_matrix(self, left, right, bottom, top, near, far, fov=None):
        mp = np.eye(4)
        mp.itemset(0, 2 / (right - left))
        mp.itemset(3, -(right + left) / (right - left))
        mp.itemset(5, 2 / (top - bottom))
        mp.itemset(7, -(top + bottom) / (top - bottom))
        mp.itemset(10, -2 / (far - near))
        mp.itemset(11, -(far + near) / (far - near))
        return mp

class PerspectiveViewport(Viewport):

    def calculate_projection_matrix(self, left, right, bottom, top, near, far, fov):
        mp = np.eye(4)
        mp.itemset(0, 2 * near / (right - left))
        mp.itemset(2, (right + left) / (right - left))
        mp.itemset(5, 2 * near / (top - bottom))
        mp.itemset(6, (top + bottom) / (top - bottom))
        mp.itemset(10, -(far + near) / (far - near))
        mp.itemset(11, -(2 * far * near) / (far - near))
        mp.itemset(14, -1)
        mp.itemset(15, 0)
        return mp