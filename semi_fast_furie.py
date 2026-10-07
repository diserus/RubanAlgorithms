import math

from mycomplex import Complex

C = 5


def half_fast_forward(f, p1, p2):
    N = p1 * p2
    mul_count = 0

    A1 = [Complex() for _ in range(N)]

    for k1 in range(p1):
        for j2 in range(p2):
            acc = Complex()
            for j1 in range(p1):
                angle = 2.0 * math.pi * (j1 * k1) / p1
                e = Complex(math.cos(-angle), math.sin(-angle))
                e = e * f[j2 + p2 * j1]
                mul_count += 1
                acc = acc + e
            A1[k1 * p2 + j2] = acc * (1.0 / p1)

    A = [Complex() for _ in range(N)]

    for k1 in range(p1):
        for k2 in range(p2):
            acc = Complex()
            for j2 in range(p2):
                angle = 2.0 * math.pi * (j2 / N) * (k1 + p1 * k2)
                e = Complex(math.cos(-angle), math.sin(-angle))
                e = e * A1[k1 * p2 + j2]
                mul_count += 1
                acc = acc + e
            A[k1 + p1 * k2] = acc * (1.0 / p2)

    return A, mul_count


def half_fast_backward(A, p1, p2):
    N = p1 * p2
    mul_count = 0

    A1 = [Complex() for _ in range(N)]

    for k1 in range(p1):
        for j2 in range(p2):
            acc = Complex()
            for k2 in range(p2):
                angle = 2.0 * math.pi * (j2 / N) * (k1 + p1 * k2)
                e = Complex(math.cos(angle), math.sin(angle))
                e = e * A[k1 + p1 * k2]
                mul_count += 1
                acc = acc + e
            A1[k1 * p2 + j2] = acc

    f = [0.0] * N
    for j1 in range(p1):
        for j2 in range(p2):
            acc = Complex()
            for k1 in range(p1):
                angle = 2.0 * math.pi * (j1 * k1) / p1
                e = Complex(math.cos(angle), math.sin(angle))
                e = e * A1[k1 * p2 + j2]
                mul_count += 1
                acc = acc + e
            f[j2 + p2 * j1] = acc.real

    return f, mul_count


if __name__ == "__main__":
    f = [1.0, 3.0, -2.0, 5.0, 0.0, -1.0, 4.0, -3.0]
    N = len(f)
    p1, p2 = 2, 4

    print("f[n] =", f)

    A, fwd_mul = half_fast_forward(f, p1, p2)
    print(f"\nПрямое ППФ (A[k]) для N = {p1}*{p2} = {N}:")
    for k, val in enumerate(A):
        print(f" A[{k}] = {val.real:8.4f} + {val.imag:8.4f}j")
    print("\nТрудоёмкость ППФ:")
    print(
        f"  слагаемых: {fwd_mul}, T = c * N*(p1+p2) = {C} * {N} * ({p1}+{p2}) = {C * fwd_mul}"
    )

    f_rec, bwd_mul = half_fast_backward(A, p1, p2)
    print("\nОбратное ППФ:")
    for n, val in enumerate(f_rec):
        print(f" f[{n}] = {val.real:8.4f}")
    print("\nТрудоёмкость ОППФ:")
    print(
        f"  слагаемых: {bwd_mul}, T = c * N*(p1+p2) = {C} * {N} * ({p1}+{p2}) = {C * bwd_mul}"
    )
