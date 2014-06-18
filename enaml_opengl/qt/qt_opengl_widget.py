__author__ = 'jack'

import numpy as np

from enaml.qt import QtCore, QtOpenGL
from atom.api import Typed, Int
from enaml.qt.qt_control import QtControl

from enaml_opengl.widgets.opengl_widget import ProxyOpenGLWidget
from enaml_opengl.events import KeyEvent, MouseEvent, WheelEvent
from enaml_opengl.renderer import Renderer
from enaml_opengl.geometry import Size


class QtOGLWidget(QtOpenGL.QGLWidget):
    # class variable for sharing OpenGL Context
    _ShareWidget = None

    def __init__(self, proxy, parent=None):
        if QtOGLWidget._ShareWidget is None:
            QtOGLWidget._ShareWidget = QtOpenGL.QGLWidget()
        super(QtOGLWidget, self).__init__(parent, QtOGLWidget._ShareWidget)

        self.proxy = proxy

        # eventually handle repeating keys with timer as in pyqtgraph GLViewWidget

        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.makeCurrent()

    # opengl events
    def initializeGL(self):
        self.proxy.on_initialize_gl()

    def resizeGL(self, w, h):
        self.proxy.on_resize_gl(w, h)

    def paintGL(self):
        self.proxy.on_paint_gl()

    # user interaction events
    def mousePressEvent(self, ev):
        self.proxy.on_mouse_press_event(ev)

    def mouseReleaseEvent(self, ev):
        self.proxy.on_mouse_release_event(ev)

    def mouseMoveEvent(self, ev):
        self.proxy.on_mouse_move_event(ev)

    def wheelEvent(self, ev):
        self.proxy.on_mouse_wheel_event(ev)

    def keyPressEvent(self, ev):
        # repeat keys handling ?
        #ev.accept()
        self.proxy.on_key_press_event(ev)

    def keyReleaseEvent(self, ev):
        # repeat keys handling ?
        #ev.accept()
        self.proxy.on_key_release_event(ev)



class QtOpenGLWidget(QtControl, ProxyOpenGLWidget):
    """ A Qt implementation of an Enaml ProxyOpenGL widget.

    """

    #: A reference to the widget created by the proxy.
    widget = Typed(QtOGLWidget)

    renderer = Typed(Renderer)

    #: Cyclic notification guard. This a bitfield of multiple guards.
    _guard = Int(0)


    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying html widget.

        """

        widget = QtOGLWidget(self, self.parent_widget())
        self.widget = widget



    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(QtOpenGLWidget, self).init_widget()
        # some initialization here ?


    #--------------------------------------------------------------------------
    # OpenGLWidget callbacks
    #--------------------------------------------------------------------------
    def on_initialize_gl(self):
        if self.renderer:
            self.renderer.initialize_gl()


    def on_resize_gl(self, w, h):
        if self.renderer:
            self.renderer.resize_gl(Size(w,h))

    def on_paint_gl(self):
        if self.renderer:
            self.renderer.paint_gl()


    # just pass the interaction events through for now
    def on_mouse_press_event(self, ev):
        self.declaration.mouse_press_event(MouseEvent.from_qt(ev))

    def on_mouse_release_event(self, ev):
        self.declaration.mouse_release_event(MouseEvent.from_qt(ev))

    def on_mouse_wheel_event(self, ev):
        self.declaration.mouse_wheel_event(WheelEvent.from_qt(ev))

    def on_mouse_move_event(self, ev):
        self.declaration.mouse_move_event(MouseEvent.from_qt(ev))

    def on_key_press_event(self, ev):
        self.declaration.key_press_event(KeyEvent.from_qt(ev))

    def on_key_release_event(self, ev):
        self.declaration.key_release_event(KeyEvent.from_qt(ev))


    #--------------------------------------------------------------------------
    # OpenGLWidget API
    #--------------------------------------------------------------------------
    def set_renderer(self, renderer):
        if self.renderer:
            self.unobserve("renderer.trigger_update", self.update)
        self.renderer = renderer
        #self.update()
        self.observe("renderer.trigger_update", self.update)


    def update(self):
        """
        notify OpenGL widget to redraw
        """
        self.widget.update()
