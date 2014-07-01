__author__ = 'jack'
import numpy as np
from atom.api import Typed, Signal, Int, observe
from enaml.core.api import Declarative
from enaml.core.declarative import d_
from OpenGL.GL import *
from .camera import Camera
from .geometry import Size, Rect
from .scenegraph_node import Scene3D

#: Cyclic guard flags
RENDERING_FLAG = 0x1

class Renderer(Declarative):

    #: items
    scene = d_(Typed(Scene3D))

    #: the canvas size as reported by resizeGL
    canvas_size = d_(Typed(Size))

    #: background color
    background_color = d_(Typed(np.ndarray))

    #: trigger an update to
    trigger_update = Signal()

    #: Cyclic notification guard flags.
    _guard = d_(Int(0))

    def initialize_gl(self, widget):
        for item in self.scene.nodes:
            item.initialize_gl()
        self.scene.observe("trigger_update", self.check_trigger_update)

    def enable_trigger(self, value):
        if value:
            self._guard &= ~RENDERING_FLAG
        else:
            self._guard |= RENDERING_FLAG

    def check_trigger_update(self):
        if self._guard & RENDERING_FLAG:
            return
        self.trigger_update()

    def resize_gl(self, widget, size):
        self.canvas_size = size

    def paint_gl(self, widget):
        if self._guard & RENDERING_FLAG:
            return
        self._guard |= RENDERING_FLAG

        self.clear_screen()
        self.render(widget)
        # swap buffers manually ?

        self._guard &= ~RENDERING_FLAG

    def clear_screen(self):
        if self.background_color is not None:
            glClearColor(*self.background_color.flatten())
        glClear( GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT )

    def render_items(self, context):
        for item in self.scene.nodes:
            item.render(context.copy())

    # overwrite in renderer implementations
    def render(self, widget):
        raise NotImplementedError



class MonoRenderer(Renderer):
    #: the camera / viewpoint
    camera = d_(Typed(Camera))

    def render(self, widget):
        self.camera.setup()
        context = dict(widget=widget, camera=self.camera, canvas_size=self.canvas_size)
        self.render_items(context)

    @observe('canvas_size')
    def _update_viewport(self, change):
        box = Rect(self.camera.viewport.box.x, self.camera.viewport.box.y,
                  self.canvas_size.width, self.canvas_size.height)
        self.camera.viewport.box = box