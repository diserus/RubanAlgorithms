import math

from mycomplex import Complex

C = 5


def half_fast_forward(f, p1, p2):
    N = p1 * p2
    if N != len(f):
        raise ValueError("ППФ: длина массива должна быть равна p1 * p2")
    mul_count = 0

    A1 = [Complex() for _ in range(N)]

    for k1 in range(p1):
        for j2 in range(p2):
            acc = Complex()
            for j1 in range(p1):
                angle = 2.0 * math.pi * (j1 * k1) / p1
                e = Complex.exp(-angle) * f[j2 + p2 * j1]
                mul_count += 1
                acc = acc + e
            A1[k1 * p2 + j2] = acc / p1

    A = [Complex() for _ in range(N)]

    for k1 in range(p1):
        for k2 in range(p2):
            acc = Complex()
            for j2 in range(p2):
                angle = 2.0 * math.pi * (j2 / N) * (k1 + p1 * k2)
                e = Complex.exp(-angle) * A1[k1 * p2 + j2]
                mul_count += 1
                acc = acc + e
            A[k1 + p1 * k2] = acc / p2

    return A, mul_count


def half_fast_backward(A, p1, p2):
    N = p1 * p2
    if N != len(A):
        raise ValueError("ППФ: длина массива должна быть равна p1 * p2")
    mul_count = 0

    A1 = [Complex() for _ in range(N)]

    for k1 in range(p1):
        for j2 in range(p2):
            acc = Complex()
            for k2 in range(p2):
                angle = 2.0 * math.pi * (j2 / N) * (k1 + p1 * k2)
                e = Complex.exp(angle) * A[k1 + p1 * k2]
                mul_count += 1
                acc = acc + e
            A1[k1 * p2 + j2] = acc

    f = [0.0] * N
    for j1 in range(p1):
        for j2 in range(p2):
            acc = Complex()
            for k1 in range(p1):
                angle = 2.0 * math.pi * (j1 * k1) / p1
                e = Complex.exp(angle) * A1[k1 * p2 + j2]
                mul_count += 1
                acc = acc + e
            f[j2 + p2 * j1] = acc.real

    return f, mul_count

def fast_furie(f):
    n = len(f)
    if n == 0:
        return [], 0
    if n == 1:
        return list(f), 0
    if n % 2 != 0:
        return None

    p1 = 2
    p2 = n // 2
    mul_count = 0

    A1 = [[Complex() for _ in range(p2)] for _ in range(p1)]
    for j2 in range(p2):
        s = f[j2] + f[j2 + p2]
        d = f[j2] - f[j2 + p2]
        A1[0][j2] = s / p1
        A1[1][j2] = d * Complex.exp(-2 * math.pi * j2 / n) / p1
        mul_count += 1

    B = [fast_furie(A1[k1]) for k1 in range(p1)]
    mul_count += sum(count for _, count in B)
    B = [spectrum for spectrum, _ in B]

    result = [Complex() for _ in range(n)]
    for k1 in range(p1):
        for k2 in range(p2):
            result[k1 + p1 * k2] = B[k1][k2]

    return result, mul_count


def _to_complex(value):
    return value if isinstance(value, Complex) else Complex(value)


def _fast_furie_backward(A):
    n = len(A)
    if n == 0:
        return [], 0
    if n == 1:
        return [_to_complex(A[0])], 0
    if n % 2 != 0:
        return None

    p1 = 2
    p2 = n // 2
    mul_count = 0

    A1 = [[Complex() for _ in range(p2)] for _ in range(p1)]
    for k1 in range(p1):
        sub = [A[k1 + p1 * k2] for k2 in range(p2)]
        B_k1, sub_mul = _fast_furie_backward(sub)
        mul_count += sub_mul
        angle = 2.0 * math.pi * k1 / n
        for j2 in range(p2):
            if k1 == 0:
                A1[k1][j2] = B_k1[j2]
            else:
                A1[k1][j2] = B_k1[j2] * Complex.exp(angle * j2)
                mul_count += 1

    result = [Complex() for _ in range(n)]
    for j2 in range(p2):
        result[j2] = A1[0][j2] + A1[1][j2]
        result[j2 + p2] = A1[0][j2] - A1[1][j2]

    return result, mul_count


def fast_furie_backward(A):
    result, mul_count = _fast_furie_backward(A)
    return [z.real for z in result], mul_count



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

    r = N.bit_length() - 1
    A_fft, fft_mul = fast_furie(f)
    print(f"\nБПФ (рекурсивная версия), N = 2^{r} = {N}:")
    for k, val in enumerate(A_fft):
        print(f" A[{k}] = {val.real:8.4f} + {val.imag:8.4f}j")
    print("\nТрудоёмкость БПФ:")
    print(
        f"  умножений: {fft_mul}, T = c * N*log2(N) = {C} * {N} * {r} = {C * fft_mul}"
    )

    f_rec_fft, fft_bwd_mul = fast_furie_backward(A_fft)
    print("\nОбратное БПФ:")
    for n, val in enumerate(f_rec_fft):
        print(f" f[{n}] = {val:8.4f}")
    print("\nТрудоёмкость ОБПФ:")
    print(
        f"  умножений: {fft_bwd_mul}, T = c * N*log2(N) = {C} * {N} * {r} = {C * fft_bwd_mul}"
    )
