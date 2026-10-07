import math


class Complex:
    __slots__ = ("imag", "real")

    def __init__(self, real=0.0, imag=0.0):
        self.real = float(real)
        self.imag = float(imag)

    def __repr__(self):
        return f"{self.real:.6g}{self.imag:+.6g}j"

    def __add__(self, other):
        if isinstance(other, Complex):
            return Complex(self.real + other.real, self.imag + other.imag)
        if isinstance(other, (int, float)):
            return Complex(self.real + other, self.imag)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Complex):
            return Complex(self.real - other.real, self.imag - other.imag)
        if isinstance(other, (int, float)):
            return Complex(self.real - other, self.imag)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Complex):
            return Complex(
                self.real * other.real - self.imag * other.imag,
                self.real * other.imag + self.imag * other.real,
            )
        if isinstance(other, (int, float)):
            return Complex(self.real * other, self.imag * other)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Complex):
            denom = other.real**2 + other.imag**2
            return Complex(
                (self.real * other.real + self.imag * other.imag) / denom,
                (self.imag * other.real - self.real * other.imag) / denom,
            )
        if isinstance(other, (int, float)):
            return Complex(self.real / other, self.imag / other)
        return NotImplemented

    def __abs__(self):
        return math.hypot(self.real, self.imag)
