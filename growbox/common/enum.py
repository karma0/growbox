# -*- cosing: utf-8 -*-

"""Enumeration base class overrides"""

from enum import Enum as EnumBase


class Enum(EnumBase):

    # Binary operators

    def __add__(self, other):
        return self.value + other

    def __sub__(self, other):
        return self.value - other

    def __mul__(self, other):
        return self.value * other

    def __floordiv__(self, other):
        return self.value // other

    def __truediv__(self, other):
        return self.value / other

    def __mod__(self, other):
        return self.value % other

    def __pow__(self, other, *modulo):
        return self.value ** other

    def __lshift__(self, other):
        return self.value << other

    def __rshift__(self, other):
        return self.value >> other

    def __and__(self, other):
        return self.value & other

    def __xor__(self, other):
        return self.value ^ other

    def __or__(self, other):
        return self.value | other

    # Extended assignments

    def __iadd__(self, other):
        self.value += other

    def __isub__(self, other):
        self.value -= other

    def __imul__(self, other):
        self.value *= other

    def __ifloordiv__(self, other):
        self.value //= other

    def __idiv__(self, other):
        self.value /= other

    def __imod__(self, other):
        self.value %= other

    def __ipow__(self, other, *modulo):
        self.value **= other

    def __ilshift__(self, other):
        self.value <<= other

    def __irshift__(self, other):
        self.value >>= other

    def __iand__(self, other):
        self.value &= other

    def __ixor__(self, other):
        self.value ^= other

    def __ior__(self, other):
        self.value |= other

    # Unary operators

    def __neg__(self):
        return -self.value

    def __pos__(self):
        return +self.value

    def __abs__(self):
        return abs(self.value)

    def __invert__(self):
        return ~self.value

    def __complex__(self):
        return complex(self.value)

    def __int__(self):
        return int(self.value)

    def __long__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __oct__(self):
        return oct(self.value)

    def __hex__(self):
        return hex(self.value)

    # Comparison

    def __lt__(self, other):
        return self.value < other

    def __le__(self, other):
        return self.value <= other

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other

    def __ge__(self, other):
        return self.value >= other

    def __gt__(self, other):
        return self.value > other
