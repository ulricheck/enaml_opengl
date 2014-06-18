__author__ = 'jack'

from atom.api import Atom, Enum, Typed, Value, Dict, List, Event
from enaml.layout.geometry import Size, Pos, Box, Rect
from enaml.layout.geometry import SizeF, PosF, BoxF, RectF

from enaml.layout.geometry import Pos as Vec2i
from enaml.layout.geometry import PosF as Vec2d


class BaseVec3(tuple):
    """ A tuple subclass representing (x, y, z) positions. Subclasses
    should override the __new__ method to enforce any necessary typing.

    """
    __slots__ = ()

    @staticmethod
    def coerce_type(item):
        return item

    def __new__(cls, x=None, y=None, z=None):
        if isinstance(x, (tuple, BaseVec3)):
            return cls(*x)
        c = cls.coerce_type
        x = c(x)
        y = c(y)
        z = c(z)
        return super(BaseVec3, cls).__new__(cls, (x, y, z))

    def __getnewargs__(self):
        return tuple(self)

    def __repr__(self):
        template = '%s(x=%s, y=%s, z=%s)'
        values = (self.__class__.__name__,) + self
        return template % values

    @property
    def x(self):
        """ The 'x' component of the position.

        """
        return self[0]

    @property
    def y(self):
        """ The 'y' component of the position.

        """
        return self[1]

    @property
    def z(self):
        """ The 'z' component of the position.

        """
        return self[2]




class Vec3i(BaseVec3):
    """ An implementation of BasePos for integer values.

    """
    __slots__ = ()

    @staticmethod
    def coerce_type(item):
        return 0 if item is None else int(item)


class Vec3d(BaseVec3):
    """ An implementation of BasePos of floating point values.

    """
    __slots__ = ()

    @staticmethod
    def coerce_type(item):
        return 0.0 if item is None else float(item)







class BaseQuaternion(tuple):
    """ A tuple subclass representing (x, y, z, w) quaternions. Subclasses
    should override the __new__ method to enforce any necessary typing.

    """
    __slots__ = ()

    @staticmethod
    def coerce_type(item):
        return item

    def __new__(cls, x=None, y=None, z=None, w=None):
        if isinstance(x, (tuple, BaseQuaternion)):
            return cls(*x)
        c = cls.coerce_type
        x = c(x)
        y = c(y)
        z = c(z)
        w = c(w)
        return super(BaseQuaternion, cls).__new__(cls, (x, y, z, w))

    def __getnewargs__(self):
        return tuple(self)

    def __repr__(self):
        template = '%s(x=%s, y=%s, z=%s, w=%s)'
        values = (self.__class__.__name__,) + self
        return template % values

    @property
    def x(self):
        """ The 'x' component of the rotation.

        """
        return self[0]

    @property
    def y(self):
        """ The 'y' component of the rotation.

        """
        return self[1]

    @property
    def z(self):
        """ The 'z' component of the rotation.

        """
        return self[2]

    @property
    def w(self):
        """ The 'w' component of the rotation.

        """
        return self[3]



class Quaternion(BaseQuaternion):
    """ An implementation of Quaternion of floating point values.

    """
    __slots__ = ()

    @staticmethod
    def coerce_type(item):
        return 0.0 if item is None else float(item)

