__author__ = 'jack'

from enaml.qt import QtCore, QtGui, QtOpenGL
from OpenGL.GL import *
import OpenGL.GL.framebufferobjects as glfbo

from atom.api import Typed, Value, Dict, List, Event
from enaml.qt.qt_control import QtControl

from enaml_opengl.widgets.opengl_widget import ProxyOpenGLWidget
from enaml_opengl.widgets.camera import Camera


class QtOGLWidget(QtOpenGL.QGLWidget):
    # class variable for sharing OpenGL Context
    _ShareWidget = None

    def __init__(self, proxy, parent=None):
        if QtOGLWidget._ShareWidget is None:
            QtOGLWidget._ShareWidget = QtOpenGL.QGLWidget()
        super(QtOGLWidget, self).__init__(parent, QtOGLWidget._ShareWidget)

        self.proxy = proxy

        # eventually handle repeating keys with timer as in pyqtgraph GLViewWidget

        self.widget.setFocusPolicy(QtCore.Qt.ClickFocus)
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
        self.proxy.on_key_press_event(ev)

    def keyReleaseEvent(self, ev):
        self.proxy.on_key_release_event(ev)



class QtOpenGLWidget(QtControl, ProxyOpenGLWidget):
    """ A Qt implementation of an Enaml ProxyOpenGL widget.

    """

    #: A reference to the widget created by the proxy.
    widget = Typed(QtOGLWidget)

    camera = Typed(Camera)
    scene = Value()

    background_color = Typed(np.ndarray)

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
        pass


    def on_resize_gl(self, w, h):
        vp = self.camera.viewport
        # combine into one transaction
        vp.width = w
        vp.height = h



    def on_paint_gl(self):

        # set projection and modelview matrix
        self.camera.render()

        # clear screen
        glClearColor(*self.declaration.background_color.flatten())
        glClear( GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT )

        self.scene.render()


    def update(self):
        """
        notify OpenGL widget to redraw
        """
        self.widget.update()


    # just pass the interaction events through for now
    def on_mouse_press_event(self, ev):
        self.declaration.mouse_press_event(ev)

    def on_mouse_release_event(self, ev):
        self.declaration.mouse_release_event(ev)

    def on_mouse_wheel_event(self, ev):
        self.declaration.mouse_wheel_event(ev)

    def on_mouse_move_event(self, ev):
        self.declaration.mouse_move_event(ev)

    def on_key_press_event(self, ev):
        self.declaration.key_press_event(ev)

    def on_key_release_event(self, ev):
        self.declaration.key_release_event(ev)


    #--------------------------------------------------------------------------
    # OpenGLWidget API
    #--------------------------------------------------------------------------
    def set_camera(self, camera):
        self.camera = camera
        self.update()

    def set_scene(self, scene):
         self.scene = scene
         self.update()
