import copy


class GeoLocation:
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    def copy(self):
        return copy.deepcopy(self)

    def x(self):
        return self._x

    def y(self):
        return self._y

    def z(self):
        return self._z
