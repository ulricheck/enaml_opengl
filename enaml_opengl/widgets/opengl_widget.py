__author__ = 'jack'

from atom.api import Typed, ForwardTyped, observe, set_default, Signal
from enaml.core.declarative import d_
from enaml.widgets.control import Control, ProxyControl


from enaml_opengl.renderer import Renderer
from enaml_opengl.events import MouseHandler, KeyHandler


class ProxyOpenGLWidget(ProxyControl):
    """ The abstract definition of a proxy QtOpenGL.QGLWidget object.

    """
    #: A reference to the OpenGLWidget declaration.
    declaration = ForwardTyped(lambda: OpenGLWidget)

    def set_renderer(self, renderer):
         raise NotImplementedError

    def set_mouse_handler(self, mouse_handler):
         raise NotImplementedError

    def set_key_handler(self, key_handler):
         raise NotImplementedError

    def update(self, *args):
        raise NotImplementedError


class OpenGLWidget(Control, MouseHandler, KeyHandler):
    """ An extremely simple widget for displaying OpenGL.

    """

    #: the renderer for the widget
    renderer = d_(Typed(Renderer))

    #: trigger a widget update
    update = d_(Signal())

    mouse_handler = d_(Typed(MouseHandler))
    key_handler = d_(Typed(KeyHandler))

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
        if self.renderer:
            self.unobserve("renderer.trigger_update", self.proxy.update)
        super(OpenGLWidget, self)._update_proxy(change)
        self.observe("renderer.trigger_update", self.proxy.update)

    @observe('update')
    def _update_canvas(self, *args):
        """ An observer which propagates update events to the widget
        """
        self.proxy.update()


    @observe('mouse_handler', 'key_handler')
    def _update_handlers(self, change):
        """ An observer which connects key/mouse handlers
        """
        super(OpenGLWidget, self)._update_proxy(change)

