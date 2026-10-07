"""Специальная библиотека для работы с комплексными числами.

Содержит только операции, используемые в furie.py (ДПФ, полубыстрое ПФ, БПФ):
создание числа, сложение, вычитание, умножение,
деление на скаляр и модуль.
"""

import math


class Complex:
    """Комплексное число вида real + imag*j."""

    __slots__ = ("real", "imag")

    def __init__(self, real=0.0, imag=0.0):
        self.real = float(real)
        self.imag = float(imag)

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
            denom = other.real ** 2 + other.imag ** 2
            return Complex(
                (self.real * other.real + self.imag * other.imag) / denom,
                (self.imag * other.real - self.real * other.imag) / denom,
            )
        if isinstance(other, (int, float)):
            return Complex(self.real / other, self.imag / other)
        return NotImplemented

    def __abs__(self):
        """Модуль комплексного числа."""
        return math.hypot(self.real, self.imag)
