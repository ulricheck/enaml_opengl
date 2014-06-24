__author__ = 'jack'

from atom.api import Value, Typed, ForwardTyped, observe, set_default, Event
from enaml.core.declarative import d_
from enaml.widgets.control import Control, ProxyControl


from enaml_opengl.renderer import Renderer
from enaml_opengl.events import KeyEvent, MouseEvent, WheelEvent
from enaml_opengl.geometry import Size


class ProxyOpenGLWidget(ProxyControl):
    """ The abstract definition of a proxy QtOpenGL.QGLWidget object.

    """
    #: A reference to the OpenGLWidget declaration.
    declaration = ForwardTyped(lambda: OpenGLWidget)

    def set_renderer(self, renderer):
         raise NotImplementedError

    def update(self):
        raise NotImplementedError


class OpenGLWidget(Control):
    """ An extremely simple widget for displaying OpenGL.

    """

    #: size of the canvas in pixels
    size = d_(Typed(Size))

    #: the renderer for the widget
    renderer = d_(Typed(Renderer))

    #: trigger a widget update
    update = d_(Event(), writable=False)

    #: interaction events
    mouse_press_event = d_(Event(MouseEvent), writable=False)
    mouse_release_event = d_(Event(MouseEvent), writable=False)
    mouse_wheel_event = d_(Event(WheelEvent), writable=False)
    mouse_move_event = d_(Event(MouseEvent), writable=False)
    key_press_event = d_(Event(KeyEvent), writable=False)
    key_release_event = d_(Event(KeyEvent), writable=False)

    #: An opengl control expands freely in height and width by default.
    hug_width = set_default('ignore')
    hug_height = set_default('ignore')

    #: A reference to the ProxyOpenGLWidget object
    proxy = Typed(ProxyOpenGLWidget)

    #--------------------------------------------------------------------------
    # Observers
    #--------------------------------------------------------------------------
    @observe('renderer', )
    def _update_proxy(self, change):
        """ An observer which sends state change to the proxy.
        """
        # The superclass handler implementation is sufficient.
        if self.renderer:
            self.unobserve("renderer.trigger_update", self.proxy.update)
        super(OpenGLWidget, self)._update_proxy(change)
        self.observe("renderer.trigger_update", self.proxy.update)

    @observe('update')
    def _update_canvas(self, change):
        """ An observer which propagates update events to the widget
        """
        self.proxy.update()
