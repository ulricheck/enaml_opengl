__author__ = 'jack'
import numpy as np
from atom.api import Atom, List, Dict, Typed, Bool, Float, Unicode, ForwardTyped
from OpenGL.GL import *
from OpenGL import GL

from .util import print_exception


class SceneGraphNode(Atom):

    #: node id
    id = Unicode()

    #: is node visible
    visible = Bool(True)

    #: depth of this node
    depth = Float(0)

    #: local transform
    transform = Typed(np.ndarray, factory=lambda: np.identity(4))

    #: parent node
    parent = ForwardTyped(lambda: SceneGraphNode)

    #: children of this node
    children = List(ForwardTyped(lambda: SceneGraphNode))

    @property
    def node_path(self):
        if self.parent is not None:
            return "%s/%s" % (self.parent.node_path, self.id)
        return id

    def initialize(self):
        self.initialize_node()
        for item in self.children:
            item.initialize()

    def render(self, context):
        # render all items including self in the correct order
        items = self.children[:]
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
                    print(msg)
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


    # management
    def add_child(self, node):
        node.parent = self
        # XXX does append notifiy on change ???
        self.children.append(node)


    # implementation stubs
    def initialize_node(self):
        pass


    def render_node(self, context):
        """
        render this node, overwrite this method to implement opengl output
        """
        pass


class GraphicsNode(SceneGraphNode):

    #: options to be set before rendering
    gl_options = Dict()

    def setup_gl(self):
        for k,v in self.gl_options.items()
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
