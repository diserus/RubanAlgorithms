from furie import dft, idft


def conv(a, b):
    n = len(a)
    m = len(b)
    c = [0.0] * (n + m - 1)
    for i in range(n):
        for k in range(m):
            c[i + k] += a[i] * b[k]
    return c


def conv_dft(a, b):
    n = len(a)
    m = len(b)
    L = n + m - 1
    ap = [float(x) for x in a] + [0.0] * (L - n)
    bp = [float(x) for x in b] + [0.0] * (L - m)
    A = dft(ap)
    B = dft(bp)
    P = [A[k] * B[k] for k in range(L)]
    return [v.real * L for v in idft(P)]


if __name__ == "__main__":
    a = [1.0, 2.0, 3.0]
    b = [2.0, 3.0]

    print("a =", a)
    print("b =", b)

    direct = conv(a, b)
    via_dft = conv_dft(a, b)

    print("\nПрямая свёртка:")
    for i, v in enumerate(direct):
        print(f" c[{i}] = {v:8.4f}")

    print("\nСвёртка через ДПФ:")
    for i, v in enumerate(via_dft):
        print(f" c[{i}] = {v:8.4f}")
