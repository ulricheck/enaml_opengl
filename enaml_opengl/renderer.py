__author__ = 'jack'
import numpy as np
from atom.api import Atom, Typed, Event, List, observe
from OpenGL.GL import (glMatrixMode, glLoadIdentity, glMultMatrixf,
            glClearColor, glClear,
            GL_PROJECTION, GL_MODELVIEW)

from .viewport import Viewport, PerspectiveViewport
from .camera import Camera, PinholeCamera
from .geometry import Size
from .scenegraph_node import SceneGraphNode

class Renderer(Atom):

    #: items
    nodes = List(SceneGraphNode)


    #: the canvas size as reported by resizeGL
    canvas_size = Typed(Size)

    #: background color
    background_color = Typed(np.ndarray)

    #: trigger an update to
    trigger_update = Event()

    def initialize_gl(self):
        for item in self.nodes:
            item.initialize()

    def resize_gl(self, size):
        self.size = size

    def paint_gl(self):
        self.clear_screen()
        self.render()
        # swap buffers manually ?

    def clear_screen(self):
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
        self.camera.viewport.box.width = self.canvas_size.width
        self.camera.viewport.box.height = self.canvas_size.height