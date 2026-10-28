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
    if N != len(A):
        raise ValueError("ППФ: длина массива должна быть равна p1 * p2")
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


def _bit_reverse(value, bits):
    result = 0
    for _ in range(bits):
        result = (result << 1) | (value & 1)
        value >>= 1
    return result


def _forward_steps(A_0, r):
    N = len(A_0)
    A_s = A_0
    mul_count = 0

    for s in range(r):
        A_next = [Complex() for _ in range(N)]

        for k in range(1 << s):
            K_s = _bit_reverse(k, s)
            angle = -2.0 * math.pi * K_s / (1 << (s + 1))
            w = Complex(math.cos(angle), math.sin(angle))

            for j in range(1 << (r - s - 1)):
                i0 = ((2 * k) << (r - s - 1)) | j
                i1 = i0 | (1 << (r - s - 1))
                A_j0 = A_s[i0]
                A_j1 = A_s[i1]
                A_next[i0] = (A_j0 + w * A_j1) * 0.5
                A_next[i1] = (A_j0 - w * A_j1) * 0.5
                mul_count += 2

        A_s = A_next

    return A_s, mul_count


def _backward_steps(A_r, r):
    N = len(A_r)
    A_s = A_r
    mul_count = 0

    for s in range(r - 1, -1, -1):
        A_prev = [Complex() for _ in range(N)]

        for k in range(1 << s):
            K_s = _bit_reverse(k, s)
            angle = 2.0 * math.pi * K_s / (1 << (s + 1))
            w = Complex(math.cos(angle), math.sin(angle))

            for j in range(1 << (r - s - 1)):
                i0 = ((2 * k) << (r - s - 1)) | j
                i1 = i0 | (1 << (r - s - 1))
                A_k0 = A_s[i0]
                A_k1 = A_s[i1]
                A_prev[i0] = A_k0 + A_k1
                A_prev[i1] = w * (A_k0 - A_k1)
                mul_count += 2

        A_s = A_prev

    return A_s, mul_count


def fast_forward(f):
    N = len(f)
    if N == 0 or N & (N - 1):
        raise ValueError("БПФ: длина массива должна быть степенью двойки")

    r = N.bit_length() - 1

    A_0 = [Complex(v.real, v.imag) if isinstance(v, Complex) else Complex(v) for v in f]
    A_r, mul_count = _forward_steps(A_0, r)

    X = [Complex() for _ in range(N)]
    for k in range(N):
        X[k] = A_r[_bit_reverse(k, r)]

    return X, mul_count


def fast_backward(X):
    N = len(X)
    if N == 0 or N & (N - 1):
        raise ValueError("БПФ: длина массива должна быть степенью двойки")

    r = N.bit_length() - 1

    A_r = [Complex() for _ in range(N)]
    for position in range(N):
        k = _bit_reverse(position, r)
        A_r[position] = Complex(X[k].real, X[k].imag)

    A_0, mul_count = _backward_steps(A_r, r)

    return [z.real for z in A_0], mul_count



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
    A_fft, fft_mul = fast_forward(f)
    print(f"\nБПФ (формула 2.4), N = 2^{r} = {N}:")
    for k, val in enumerate(A_fft):
        print(f" A[{k}] = {val.real:8.4f} + {val.imag:8.4f}j")
    print("\nТрудоёмкость БПФ:")
    print(
        f"  умножений: {fft_mul}, T = c * N*log2(N) = {C} * {N} * {r} = {C * fft_mul}"
    )

    f_rec_fft, fft_bwd_mul = fast_backward(A_fft)
    print("\nОбратное БПФ:")
    for n, val in enumerate(f_rec_fft):
        print(f" f[{n}] = {val:8.4f}")
    print("\nТрудоёмкость ОБПФ:")
    print(
        f"  умножений: {fft_bwd_mul}, T = c * N*log2(N) = {C} * {N} * {r} = {C * fft_bwd_mul}"
    )
