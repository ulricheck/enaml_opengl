__author__ = 'jack'
import numpy as np

from atom.api import Typed, Float, Int, observe
from enaml.core.declarative import d_

from .geometry import Size, Pos
from .events import MouseHandler, KeyHandler
from .external import transformations as tf

#: Cyclic guard flags
INIT_DATA_FLAG = 0x1
UPDATE_DATA_FLAG = 0x2


class ArcballCameraControl(MouseHandler, KeyHandler):

    window_size = d_(Typed(Size))

    modelview_matrix = d_(Typed(np.ndarray, factory=lambda: np.eye(4)))

    position = d_(Typed(np.ndarray))
    orientation = d_(Typed(np.ndarray))

    sensitivity = d_(Float(0.05))

    #: Cyclic notification guard flags.
    _guard = d_(Int(0))

    arcball = Typed(tf.Arcball,)
    last_mouse_position = Typed(Pos)

    BT_ROTATE = ("left", "shift")
    BT_PAN = ("left", "ctrl")

    def _get_center_radius(self):
        w = self.window_size.width
        h = self.window_size.height
        m = min(w,h)
        return (int(w/2), int(h/2)), int(m/2)


    @observe('mouse_press_event', 'mouse_move_event', 'mouse_release_event', 'mouse_wheel_event')
    def _handle_events(self, change):
        name = change['name']
        value = change['value']

        if name == "mouse_press_event":
            pos = value.position
            self.last_mouse_position = value.position

            if self.BT_ROTATE[0] in value.buttons and self.BT_ROTATE[1] in value.modifiers:
                self.arcball = tf.Arcball(initial=np.linalg.inv(self.orientation))
                self.arcball.place(*self._get_center_radius())
                self.arcball.down((pos.x, pos.y))

            # elif self.BT_PAN[0] in value.buttons and self.BT_PAN[1] in value.modifiers:
            #     pass

        elif name == "mouse_move_event":
            pos = value.position
            if self.BT_ROTATE[0] in value.buttons and self.BT_ROTATE[1] in value.modifiers:
                if self.arcball is not None:
                    self.arcball.drag((pos.x, pos.y))
                    self.orientation = np.linalg.inv(self.arcball.matrix())

            elif self.BT_PAN[0] in value.buttons and self.BT_PAN[1] in value.modifiers:
                if value.position != self.last_mouse_position:
                    print value.position, self.last_mouse_position
                    dx = value.position.x - self.last_mouse_position.x
                    dy = value.position.y - self.last_mouse_position.y

                    t = np.array([-dx, dy, 0, 0]).T

                    self.position = self.position - np.dot(self.orientation, t) * self.sensitivity
                    self.last_mouse_position = value.position

        elif name == "mouse_wheel_event":
            if self.BT_PAN[1] in value.modifiers:
                dz = float(value.delta) / 60.
                t = np.array([0, 0, dz, 0]).T
                self.position = self.position + np.dot(self.orientation, t) * self.sensitivity


        elif name == "mouse_release_event":
            pos = value.position
            if self.BT_ROTATE[0] not in value.buttons and self.BT_ROTATE[1] in value.modifiers:
                self.arcball = None

    @observe("position", "orientation")
    def _update_modelview_matrix(self, change):
        # if self._guard & INIT_DATA_FLAG or self._guard & UPDATE_DATA_FLAG:
        #     return
        #
        # self._guard |= UPDATE_DATA_FLAG

        tm = tf.translation_matrix(self.position[:3])
        om = self.orientation
        self.modelview_matrix = np.dot(tm, om)

        # self._guard &= ~UPDATE_DATA_FLAG

