__author__ = 'jack'
import numpy as np
from atom.api import Value, Coerced, Bool, observe
from OpenGL.GL import *
from enaml_opengl.scenegraph_node import GraphicsNode, d_
from enaml_opengl import shaders

class ScatterPlotItem(GraphicsNode):
    """ An LinePlot Item

    """

    #: (N,3) array of floats specifying line point locations.
    pos = d_(Coerced(np.ndarray, coercer=np.ndarray))

    #: (N,4) array of floats (0.0-1.0) specifying pot colors
    #: OR a tuple of floats specifying a single color for all spots.
    color = d_(Value([1.0, 1.0, 1.0, 0.5]))

    size = d_(Value(1.0))

    px_mode = d_(Bool(True))

    @observe("pos", "color", "size", "px_mode")
    def _spi_trigger_update(self, change):
        self.trigger_update()


    _point_texture = Value()
    _shader = Value()

    def initialize_node(self):
        ## Generate texture for rendering points
        w = 64
        def fn(x,y):
            r = ((x-w/2.)**2 + (y-w/2.)**2) ** 0.5
            return 255 * (w/2. - np.clip(r, w/2.-1.0, w/2.))
        pData = np.empty((w, w, 4))
        pData[:] = 255
        pData[:,:,3] = np.fromfunction(fn, pData.shape[:2])
        pData = pData.astype(np.ubyte)

        self._point_texture = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self._point_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, pData.shape[0], pData.shape[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, pData)

        self._shader = shaders.getShaderProgram('pointSprite')

    def render_node(self, context):
        super(ScatterPlotItem, self).render_node(context)
        widget = context.get("widget", None)

        glEnable(GL_POINT_SPRITE)

        glActiveTexture(GL_TEXTURE0)
        glEnable( GL_TEXTURE_2D )
        glBindTexture(GL_TEXTURE_2D, self._point_texture)

        glTexEnvi(GL_POINT_SPRITE, GL_COORD_REPLACE, GL_TRUE)
        #glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)    ## use texture color exactly
        #glTexEnvf( GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE )  ## texture modulates current color
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glEnable(GL_PROGRAM_POINT_SIZE)


        with self._shader:
            #glUniform1i(self.shader.uniform('texture'), 0)  ## inform the shader which texture to use
            glEnableClientState(GL_VERTEX_ARRAY)
            try:
                pos = self.pos
                #if pos.ndim > 2:
                    #pos = pos.reshape((reduce(lambda a,b: a*b, pos.shape[:-1]), pos.shape[-1]))
                glVertexPointerf(pos)

                if isinstance(self.color, np.ndarray):
                    glEnableClientState(GL_COLOR_ARRAY)
                    glColorPointerf(self.color)
                else:
                    glColor4f(*self.color)

                if not self.px_mode or isinstance(self.size, np.ndarray):
                    glEnableClientState(GL_NORMAL_ARRAY)
                    norm = np.empty(pos.shape)
                    if self.px_mode or widget is None:
                        norm[...,0] = self.size
                    else:
                        # XXX not yet implemented
                        raise NotImplementedError
                        gpos = self.mapToView(pos.transpose()).transpose()
                        pxSize = self.view().pixelSize(gpos)
                        norm[...,0] = self.size / pxSize

                    glNormalPointerf(norm)
                else:
                    glNormal3f(self.size, 0, 0)  ## vertex shader uses norm.x to determine point size
                    #glPointSize(self.size)
                glDrawArrays(GL_POINTS, 0, int(pos.size / pos.shape[-1]))
            finally:
                glDisableClientState(GL_NORMAL_ARRAY)
                glDisableClientState(GL_VERTEX_ARRAY)
                glDisableClientState(GL_COLOR_ARRAY)
