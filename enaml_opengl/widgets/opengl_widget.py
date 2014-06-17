__author__ = 'jack'

from atom.api import Value, Typed, ForwardTyped, List, observe, set_default, Event

from enaml.core.declarative import d_

from enaml.widgets.control import Control, ProxyControl

from enaml_opengl.widgets.viewport import Viewport
from enaml_opengl.widgets.camera import Camera


class ProxyOpenGLWdiget(ProxyControl):
    """ The abstract definition of a proxy QtOpenGL.QGLWidget object.

    """
    #: A reference to the OpenGLWidget declaration.
    declaration = ForwardTyped(lambda: OpenGLWidget)

    def set_camera(self, camera):
         raise NotImplementedError

    def set_scene(self, scene):
         raise NotImplementedError

    def set_background_color(self, bgcolor):
         raise NotImplementedError



class OpenGLWidget(Control):
    """ An extremely simple widget for displaying OpenGL.

    """
    #: the camera / viewpoint
    camera = d_(Typed(Camera))

    #: the scene to be rendered (Enforce types ?)
    scene = d_(Value())

    #: background_color of opengl widget
    background_color = d_(Value())

    #: interaction events
    mouse_press_event = d_(Event(), writable=False)
    mouse_release_event = d_(Event(), writable=False)
    mouse_wheel_event = d_(Event(), writable=False)
    mouse_move_event = d_(Event(), writable=False)
    key_press_event = d_(Event(), writable=False)
    key_release_event = d_(Event(), writable=False)

    #: An opengl control expands freely in height and width by default.
    hug_width = set_default('ignore')
    hug_height = set_default('ignore')

    #: A reference to the ProxyOpenGLWidget object
    proxy = Typed(ProxyOpenGLWidget)


    #: initialize default camera
    def _default_camera(self):
        return Camera()

    #--------------------------------------------------------------------------
    # Observers
    #--------------------------------------------------------------------------
     @observe('camera', 'scene', 'background_color')
    def _update_proxy(self, change):
        """ An observer which sends state change to the proxy.
        """
        # The superclass handler implementation is sufficient.
        super(OpenGLWidget, self)._update_proxy(change)
