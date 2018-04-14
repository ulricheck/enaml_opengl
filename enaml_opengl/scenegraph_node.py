__author__ = 'jack'
import numpy as np
from atom.api import Dict, Typed, Bool, Float, Signal, ForwardTyped, observe
from enaml.core.api import Declarative
from enaml.core.declarative import d_

from OpenGL.GL import *
from OpenGL import GL

from .util import print_exception




class SceneGraphNode(Declarative):

    scene_root = ForwardTyped(lambda: Scene3D)
    def child_added(self, child):
        super(SceneGraphNode, self).child_added(child)
        if isinstance(child, SceneGraphNode):
            child.scene_root = self.scene_root

    def child_removed(self, child):
        super(SceneGraphNode, self).child_removed(child)
        if isinstance(child, SceneGraphNode):
            child.scene_root = None

    def trigger_update(self):
        self.scene_root.trigger_update()

    @property
    def node_path(self):
        return "/".join(a.name for a in reversed([self, ] + list(self.traverse_ancestors())))


    def initialize_gl(self):
        for obj in self.traverse():
            if obj is self:
                continue
            if isinstance(obj, SceneGraphNode):
                obj.initialize_gl()


    def render(self, context):
        for obj in self.traverse():
            if isinstance(obj, SceneGraphNode):
                obj.render(context)






class GraphicsSceneGraphNode(SceneGraphNode):

    #: is node visible
    visible = d_(Bool(True))

    #: depth of this node
    depth = d_(Float(0))

    #: local transform
    transform = d_(Typed(np.ndarray, factory=lambda: np.identity(4)))

    # add helpers to set translation, rotation, scale separately
    # ensure synchronisation between transform and elements, but avoid cyclic updates using a _guard

    @observe("visible", "depth", "transform")
    def _gsgn_trigger_update(self, change):
        self.trigger_update()


    def initialize_gl(self):
        super(GraphicsSceneGraphNode, self).initialize_gl()
        self.initialize_node()


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

                    glMatrixMode(GL_MODELVIEW)
                    glPushMatrix()

                    glMultMatrixf(item.transform.T)

                    item.render_node(context)
                except:
                    print_exception()
                    msg = "Error while drawing item %s." % self.node_path
                    print (msg)
                finally:
                    glMatrixMode(GL_MODELVIEW)
                    glPopMatrix()

                    glPopAttrib()
            else:
                glMatrixMode(GL_MODELVIEW)
                glPushMatrix()
                try:
                    glMultMatrixf(item.transform.T)
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
    antialias  = d_(Bool(True))

    @observe("gl_options", "antialias")
    def _gn_trigger_update(self, change):
        self.trigger_update()

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



class Group(GraphicsSceneGraphNode):
    pass


class Scene3D(Declarative):

    trigger_update = Signal()

    def child_added(self, child):
        super(Scene3D, self).child_added(child)
        if isinstance(child, SceneGraphNode):
            child.scene_root = self

    def child_removed(self, child):
        super(Scene3D, self).child_removed(child)
        if isinstance(child, SceneGraphNode):
            child.scene_root = None

    @property
    def nodes(self):
        return [c for c in self.children if isinstance(c, SceneGraphNode)]
