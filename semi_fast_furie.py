"""Полубыстрое преобразование Фурье (ППФ) для N = p1 * p2.

Реализация по методичке А.А. Рубан, Т.Э. Разинкиной
«Теория сложности вычислительных процессов и структур»,
формулы (2.3a), (2.3b).

Прямое преобразование делит результат на N (как в furie.py),
обратное — не делит.
"""

import math

from mycomplex import Complex

C = 5

op_count = 0


def reset_op_count():
  global op_count
  op_count = 0


def cmul(a, b):
  global op_count
  op_count += C
  return a * b


def W(angle):
  """Комплексная экспонента exp(i * angle)."""
  return Complex(math.cos(angle), math.sin(angle))


def semi_fast(x, p1, p2, sign=-1, normalize=True):
  """ППФ. sign = -1 прямое, +1 обратное; normalize — делить ли на p1 и p2."""
  N = p1 * p2
  s1 = 1.0 / p1 if normalize else 1.0
  s2 = 1.0 / p2 if normalize else 1.0

  # (2.3a): A1[k1][j2] = (1/p1) * sum_{j1} x[j2 + p2*j1] * exp(sign*i*j1*k1*2pi/p1)
  A1 = [[Complex(0.0, 0.0) for _ in range(p2)] for _ in range(p1)]
  for k1 in range(p1):
    for j2 in range(p2):
      for j1 in range(p1):
        A1[k1][j2] += cmul(x[j2 + p2 * j1], W(sign * 2 * math.pi * k1 * j1 / p1))
      A1[k1][j2] *= s1

  # (2.3b): X[k1 + p1*k2] = (1/p2) * sum_{j2} A1[k1][j2] * exp(sign*i*j2*(k1+p1*k2)*2pi/N)
  X = [Complex(0.0, 0.0) for _ in range(N)]
  for k1 in range(p1):
    for k2 in range(p2):
      for j2 in range(p2):
        X[k1 + p1 * k2] += cmul(A1[k1][j2], W(sign * 2 * math.pi * j2 * (k1 + p1 * k2) / N))
      X[k1 + p1 * k2] *= s2
  return X


#  Прямое и обратное преобразования
ppf = lambda x, p1, p2: semi_fast(x, p1, p2)
ppf_inv = lambda X, p1, p2: semi_fast(X, p1, p2, sign=1, normalize=False)


# ---------------------------------------------------------------------------

if __name__ == "__main__":
  x = [1.0, 3.0, -2.0, 5.0, 0.0, -1.0, 4.0, -3.0]
  N = len(x)
  p1, p2 = 2, 4               # N = p1 * p2

  print("x[n] =", x)

  reset_op_count()
  X = ppf(x, p1, p2)
  print(f"\nПолубыстрое ПФ (N = {p1}*{p2} = {N}):")
  print(" X =", [f"{v.real:.4f}{v.imag:+.4f}j" for v in X])
  print(f" T = C*N*(p1+p2) = {C}*{N}*({p1}+{p2}) = {op_count}")

  x_rec = ppf_inv(X, p1, p2)
  err = max(abs(x_rec[n].real - x[n]) for n in range(N))
  print(f"\nОбратное ППФ: ошибка = {err:.2e}")
