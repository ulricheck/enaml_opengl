__author__ = 'jack'
import numpy as np
from atom.api import Atom, List, Dict, Typed, Bool, Float, Unicode, ForwardTyped, observe
from enaml.core.api import Declarative
from enaml.core.declarative import d_

from OpenGL.GL import *
from OpenGL import GL

from .util import print_exception


class SceneGraphNode(Declarative):

    @property
    def node_path(self):
        return "/".join(a.name for a in reversed([self, ] + list(self.traverse_ancestors())))


    def render(self, context):
        for item in self.traverse():
            if isinstance(obj, SceneGraphNode):
                obj.render(context)







class GraphicsSceneGraphNode(SceneGraphNode):

    #: is node visible
    visible = d_(Bool(True))

    #: depth of this node
    depth = d_(Float(0))

    #: local transform
    transform = d_(Typed(np.ndarray, factory=lambda: np.identity(4)))


    def initialize(self):
        self.initialize_node()
        super(SceneGraphNode, self).initialize()


    def render(self, context):
        # render all items including self in the correct order
        items = [c for c in self.children if isinstance(c, SceneGraphNode)]
        items.append(self)

        # sort by depth
        items.sort(key=lambda v: v.depth)

        for item in items:
            if not item.visible:
                continue
            if item is self:
                try:
                    glPushAttrib(GL_ALL_ATTRIB_BITS)
                    # for gl debugging and object picking
                    # glLoadName(id(item))
                    # self._itemNames[id(item)] = item
                    item.render_node(context)
                except:
                    print_exception()
                    msg = "Error while drawing item %s." % self.node_path
                    print msg
                finally:
                    glPopAttrib()
            else:
                glMatrixMode(GL_MODELVIEW)
                glPushMatrix()
                try:
                    glMultMatrixf(item.transform.transpose())
                    item.render(context)
                finally:
                    glMatrixMode(GL_MODELVIEW)
                    glPopMatrix()



    # implementation stubs
    def initialize_node(self):
        pass


    def render_node(self, context):
        """
        render this node, overwrite this method to implement opengl output
        """
        pass


class GraphicsNode(GraphicsSceneGraphNode):

    #: options to be set before rendering
    gl_options = d_(Dict())

    def setup_gl(self):
        for k,v in self.gl_options.items():
            if v is None:
                continue

            if isinstance(k, basestring):
                func = getattr(GL, k)
                func(*v)
            else:
                if v is True:
                    glEnable(k)
                else:
                    glDisable(k)


    def render_node(self, context):
        self.setup_gl()


class Scene3D(Declarative):

    @property
    def nodes(self):
        return [c for c in self.children if isinstance(c, SceneGraphNode)]
