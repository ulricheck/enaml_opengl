__author__ = 'jack'
import numpy as np

from atom.api import Value, Typed, Event, observe
from enaml.core.api import Declarative
from enaml.core.declarative import d_

from .geometry import Size
from .events import MouseHandler, KeyHandler
from .external import transformations as tf

class ArcballCameraControl(MouseHandler, KeyHandler):

    arcball = Typed(tf.Arcball,)

    window_size = d_(Typed(Size))
    start_transform = d_(Typed(np.ndarray))
    new_transform = d_(Typed(np.ndarray))

    def _get_center_radius(self):
        w = self.window_size.width()
        h = self.window_size.height()
        m = min(w,h)
        return (int(w/2), int(h/2)), int(m/2)


    @observe('mouse_press_event', 'mouse_move_event', 'mouse_release_event', 'mouse_wheel_event')
    def _handle_events(self, change):
        name = change['name']
        value = change['value']

        if name == "mouse_press_event":
            pos = value.position
            if "left" in value.buttons:
                self.arcball = tf.Arcball(initial=self.start_transform)
                self.arcball.place(*self._get_center_radius())
                self.arcball.down((pos.x, pos.y))

        elif name == "mouse_move_event":
            pos = value.position
            if "left" in value.buttons:
                if self.arcball is not None:
                    self.arcball.drag((pos.x, pos.y))
                    self.new_transform = self.arcball.matrix()

        elif name == "mouse_press_event":
            pos = value.position
            if "left" in value.buttons:
                self.arcball = None
                self.start_transform = self.new_transform

    @observe("new_transform")
    def _debug(self, change):
        print self.new_transform
