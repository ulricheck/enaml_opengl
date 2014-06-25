__author__ = 'jack'
from enaml.qt import QtCore
from atom.api import Atom, Enum, Typed, Int, List, Bool, Event
from enaml.core.api import Declarative
from enaml.core.declarative import d_

from enaml_opengl.geometry import Pos


class InputEvent(Atom):

    # Qt::NoModifier	0x00000000	No modifier key is pressed.
    # Qt::ShiftModifier	0x02000000	A Shift key on the keyboard is pressed.
    # Qt::ControlModifier	0x04000000	A Ctrl key on the keyboard is pressed.
    # Qt::AltModifier	0x08000000	An Alt key on the keyboard is pressed.
    # Qt::MetaModifier	0x10000000	A Meta key on the keyboard is pressed.
    # Qt::KeypadModifier	0x20000000	A keypad button is pressed.
    # Qt::GroupSwitchModifier	0x40000000	X11 only. A Mode_switch key on the keyboard is pressed.
    modifiers = List(Enum("shift", "ctrl", "alt", "meta",))

    @staticmethod
    def _modifiers_from_qt(ev):
        m = ev.modifiers()
        r = []
        if m == 0:
            return r

        if m & QtCore.Qt.ShiftModifier:
            r.append("shift")
        if m & QtCore.Qt.ControlModifier:
            r.append("ctrl")
        if m & QtCore.Qt.AltModifier:
            r.append("alt")
        if m & QtCore.Qt.MetaModifier:
            r.append("meta")
        return r


class MouseEvent(InputEvent):

    # Qt::LeftButton	0x00000001	The left button is pressed, or an event refers to the left button. (The left button may be the right button on left-handed mice.)
    # Qt::RightButton	0x00000002	The right button.
    # Qt::MidButton	0x00000004	The middle button.
    buttons = List(Enum("left", "right", "middle"))

    global_position   = Typed(Pos)
    position   = Typed(Pos)

    @classmethod
    def from_qt(cls, ev):
        b = ev.buttons()
        buttons = []
        if b != 0:
            if b & QtCore.Qt.LeftButton:
                buttons.append("left")
            if b & QtCore.Qt.RightButton:
                buttons.append("right")
            if b & QtCore.Qt.MidButton:
                buttons.append("middle")
        p = ev.pos()
        gp = ev.globalPos()

        return cls(modifiers=cls._modifiers_from_qt(ev),
                   buttons=buttons,
                   position=Pos(p.x(), p.y()),
                   global_position=Pos(gp.x(), gp.y()),
                   )


class WheelEvent(InputEvent):

    # Qt::LeftButton	0x00000001	The left button is pressed, or an event refers to the left button. (The left button may be the right button on left-handed mice.)
    # Qt::RightButton	0x00000002	The right button.
    # Qt::MidButton	0x00000004	The middle button.
    button = Enum("left", "right", "middle", "other")
    buttons = List(Enum("left", "right", "middle", "other"))

    delta = Int()

    # Qt::Horizontal	0x1
    # Qt::Vertical	0x2
    orientation = Enum("horizontal", "vertical")

    global_position   = Typed(Pos)
    position   = Typed(Pos)

    @classmethod
    def from_qt(cls, ev):
        b = ev.buttons()
        buttons = []
        if b != 0:
            if b & QtCore.Qt.LeftButton:
                buttons.append("left")
            if b & QtCore.Qt.RightButton:
                buttons.append("right")
            if b & QtCore.Qt.MidButton:
                buttons.append("middle")
        p = ev.pos()
        gp = ev.globalPos()

        orientation = "horizontal"
        if ev.orientation() & QtCore.Qt.Vertical:
            orientation = "vertical"


        return cls(modifiers=cls._modifiers_from_qt(ev),
                   buttons=buttons,
                   position=Pos(p.x(), p.y()),
                   global_position=Pos(gp.x(), gp.y()),
                   orientation=orientation,
                   delta=ev.delta(),
                   )


class KeyEvent(InputEvent):

    count = Int()
    is_auto_repeat = Bool()
    is_modifier = Bool()
    key = Int()


    @property
    def text(self):
        return chr(self.key)

    @classmethod
    def from_qt(cls, ev):
        is_mod = ev.key() in [QtCore.Qt.AltModifier, QtCore.Qt.ControlModifier,
                              QtCore.Qt.ShiftModifier, QtCore.Qt.MetaModifier]
        return cls(modifiers=cls._modifiers_from_qt(ev),
                   is_modifier=is_mod,
                   key=ev.key(),
                   is_auto_repeat=ev.isAutoRepeat(),
                   count=ev.count(),
                   )


class MouseHandler(Declarative):
    # mouse handler
    mouse_press_event = d_(Event(MouseEvent), writable=False)
    mouse_release_event = d_(Event(MouseEvent), writable=False)
    mouse_wheel_event = d_(Event(WheelEvent), writable=False)
    mouse_move_event = d_(Event(MouseEvent), writable=False)

class KeyHandler(Declarative):
    # key handler
    key_press_event = d_(Event(KeyEvent), writable=False)
    key_release_event = d_(Event(KeyEvent), writable=False)
