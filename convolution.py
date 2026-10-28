from furie import C, dft, idft
from semi_fast_furie import (
    fast_backward,
    fast_forward,
    half_fast_backward,
    half_fast_forward,
)


def conv(a, b):
    n = len(a)
    m = len(b)
    c = [0.0] * (n + m - 1)
    for i in range(n):
        for k in range(m):
            c[i + k] += a[i] * b[k]
    return c


def _pad(values, length):
    return [float(x) for x in values] + [0.0] * (length - len(values))


def _length(a, b):
    return len(a) + len(b) - 1


def conv_dft(a, b):
    L = _length(a, b)
    if L <= 0:
        return []

    ap = _pad(a, L)
    bp = _pad(b, L)
    A = dft(ap)
    B = dft(bp)
    P = [A[k] * B[k] for k in range(L)]

    return [v.real * L for v in idft(P)]


def conv_half_fast(a, b, p1, p2):
    L = _length(a, b)
    if L <= 0:
        return []

    N = p1 * p2
    if N < L:
        raise ValueError("ППФ: p1 * p2 должно быть не меньше n + m - 1")

    ap = _pad(a, N)
    bp = _pad(b, N)

    A, _ = half_fast_forward(ap, p1, p2)
    B, _ = half_fast_forward(bp, p1, p2)
    P = [A[k] * B[k] for k in range(N)]

    c, _ = half_fast_backward(P, p1, p2)

    return [v * N for v in c[:L]]


def _fft_size(L):
    size = 1
    while size < L:
        size <<= 1
    return size


def conv_fft(a, b):
    L = _length(a, b)
    if L <= 0:
        return []

    N = _fft_size(L)
    ap = _pad(a, N)
    bp = _pad(b, N)

    A, _ = fast_forward(ap)
    B, _ = fast_forward(bp)
    P = [A[k] * B[k] for k in range(N)]

    c, _ = fast_backward(P)

    return [v * N for v in c[:L]]


if __name__ == "__main__":
    a = [1.0, 2.0, 3.0]
    b = [2.0, 3.0]

    n = len(a)
    m = len(b)
    L = n + m - 1

    p1, p2 = 2, 2
    N_half = p1 * p2
    N_fft = _fft_size(L)
    r = N_fft.bit_length() - 1

    results = [
        ("Прямая свёртка", conv(a, b), n * m),
        ("Через ДПФ", conv_dft(a, b), 3 * L * L),
        ("Через ППФ", conv_half_fast(a, b, p1, p2), 3 * N_half * (p1 + p2)),
        ("Через БПФ", conv_fft(a, b), 3 * N_fft * r),
    ]

    print("a =", a)
    print("b =", b)
    print(f"L = n + m - 1 = {L}")
    print(f"ППФ: N = {N_half} = {p1} * {p2}")
    print(f"БПФ: N = {N_fft} = 2^{r}")

    for title, c, ops in results:
        print(f"\n{title}:")
        for i, v in enumerate(c):
            print(f" c[{i}] = {v:8.4f}")
        print(f" умножений: {ops}, T = c * ops = {C} * {ops} = {C * ops}")

    direct = results[0][1]
    worst = max(abs(v - direct[i]) for _, c, _ in results for i, v in enumerate(c))
    print(f"\nмакс. расхождение с прямой свёрткой: {worst:.2e}")
