__author__ = 'jack'
import numpy as np
from atom.api import Atom, Typed, Signal, List, observe
from OpenGL.GL import *
from .viewport import Viewport, PerspectiveViewport
from .camera import Camera, PinholeCamera
from .geometry import Size, Rect
from .scenegraph_node import SceneGraphNode

class Renderer(Atom):

    #: items
    nodes = List(SceneGraphNode)


    #: the canvas size as reported by resizeGL
    canvas_size = Typed(Size)

    #: background color
    background_color = Typed(np.ndarray)

    #: trigger an update to
    trigger_update = Signal()

    def initialize_gl(self):
        for item in self.nodes:
            item.initialize()

    def resize_gl(self, size):
        self.canvas_size = size

    def paint_gl(self):
        self.clear_screen()
        self.render()
        # swap buffers manually ?

    def clear_screen(self):
        if self.background_color is not None:
            glClearColor(*self.background_color.flatten())
        glClear( GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT )

    def render_items(self, context):
        for item in self.nodes:
            item.render(context.copy())

    # overwrite in renderer implementations
    def render(self):
        raise NotImplementedError



class MonoRenderer(Renderer):
    #: the camera / viewpoint
    camera = Typed(Camera)

    def render(self):
        self.camera.setup()
        context = dict()
        self.render_items(context)

    @observe('canvas_size')
    def _update_viewport(self, change):
        box = Rect(self.camera.viewport.box.x, self.camera.viewport.box.y,
                  self.canvas_size.width, self.canvas_size.height)
        self.camera.viewport.box = box